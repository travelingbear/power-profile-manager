#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <signal.h>
#include <syslog.h>
#include <sys/stat.h>
#include <errno.h>
#include <glob.h>
#include <ctype.h>

#define BATTERY_PATH "/sys/class/power_supply/BAT0"
#define STATE_FILE "/var/run/power-profile-state"
#define CONFIG_FILE "/etc/power-profiled.conf"
#define DEFAULT_THRESHOLD 30
#define DEFAULT_INTERVAL 60

static volatile int running = 1;
static int threshold = DEFAULT_THRESHOLD;
static int interval = DEFAULT_INTERVAL;

void signal_handler(int sig) {
    running = 0;
    syslog(LOG_INFO, "Received signal %d, shutting down", sig);
}

int read_int_from_file(const char *path) {
    FILE *fp = fopen(path, "r");
    if (!fp) return -1;
    
    int value;
    if (fscanf(fp, "%d", &value) != 1) {
        fclose(fp);
        return -1;
    }
    fclose(fp);
    return value;
}

int read_string_from_file(const char *path, char *buf, size_t size) {
    FILE *fp = fopen(path, "r");
    if (!fp) return -1;
    
    if (fgets(buf, size, fp) == NULL) {
        fclose(fp);
        return -1;
    }
    fclose(fp);
    
    size_t len = strlen(buf);
    if (len > 0 && buf[len-1] == '\n')
        buf[len-1] = '\0';
    
    return 0;
}

int write_to_file(const char *path, const char *value) {
    FILE *fp = fopen(path, "w");
    if (!fp) {
        syslog(LOG_WARNING, "Failed to write to %s: %s", path, strerror(errno));
        return -1;
    }
    
    if (fprintf(fp, "%s", value) < 0) {
        syslog(LOG_WARNING, "Failed to write value to %s: %s", path, strerror(errno));
        fclose(fp);
        return -1;
    }
    
    fclose(fp);
    return 0;
}

int get_battery_level() {
    char path[256];
    snprintf(path, sizeof(path), "%s/capacity", BATTERY_PATH);
    return read_int_from_file(path);
}

int is_on_ac() {
    char path[256], status[32];
    snprintf(path, sizeof(path), "%s/status", BATTERY_PATH);
    
    if (read_string_from_file(path, status, sizeof(status)) < 0)
        return 1;
    
    return (strcmp(status, "Charging") == 0 || strcmp(status, "Full") == 0);
}

void set_cpu_epp(const char *policy) {
    glob_t globbuf;
    int ret = glob("/sys/devices/system/cpu/cpu*/cpufreq/energy_performance_preference", 
                   0, NULL, &globbuf);
    
    if (ret == 0) {
        for (size_t i = 0; i < globbuf.gl_pathc; i++) {
            write_to_file(globbuf.gl_pathv[i], policy);
        }
        globfree(&globbuf);
    } else {
        syslog(LOG_WARNING, "No EPP files found");
    }
}

void set_turbo_boost(int enable) {
    // Intel: no_turbo (inverted logic: 1=disabled, 0=enabled)
    if (access("/sys/devices/system/cpu/intel_pstate/no_turbo", F_OK) == 0) {
        write_to_file("/sys/devices/system/cpu/intel_pstate/no_turbo", 
                     enable ? "0" : "1");
    }
    // AMD/Other: boost (normal logic: 1=enabled, 0=disabled)
    else if (access("/sys/devices/system/cpu/cpufreq/boost", F_OK) == 0) {
        write_to_file("/sys/devices/system/cpu/cpufreq/boost", 
                     enable ? "1" : "0");
    } else {
        syslog(LOG_WARNING, "No turbo boost control found");
    }
}

void apply_powersave() {
    set_cpu_epp("power");
    set_turbo_boost(0);
    
    if (write_to_file("/sys/firmware/acpi/platform_profile", "low-power") < 0) {
        syslog(LOG_DEBUG, "Platform profile not available or failed");
    }
    
    syslog(LOG_INFO, "Applied POWERSAVE profile");
}

void apply_balanced() {
    set_cpu_epp("balance_power");
    set_turbo_boost(1);
    
    if (write_to_file("/sys/firmware/acpi/platform_profile", "balanced") < 0) {
        syslog(LOG_DEBUG, "Platform profile not available or failed");
    }
    
    syslog(LOG_INFO, "Restored BALANCED profile (battery above threshold)");
}

char* get_current_state() {
    static char state[32];
    if (read_string_from_file(STATE_FILE, state, sizeof(state)) < 0)
        return NULL;
    return state;
}

void set_state(const char *state) {
    write_to_file(STATE_FILE, state);
}

void clear_state() {
    unlink(STATE_FILE);
}

char* trim_whitespace(char *str) {
    char *end;
    
    while(isspace((unsigned char)*str)) str++;
    
    if(*str == 0) return str;
    
    end = str + strlen(str) - 1;
    while(end > str && isspace((unsigned char)*end)) end--;
    
    end[1] = '\0';
    return str;
}

void load_config() {
    FILE *fp = fopen(CONFIG_FILE, "r");
    if (!fp) {
        syslog(LOG_INFO, "No config file found, using defaults (threshold=%d, interval=%d)", 
               DEFAULT_THRESHOLD, DEFAULT_INTERVAL);
        return;
    }
    
    char line[256];
    while (fgets(line, sizeof(line), fp)) {
        if (line[0] == '#' || line[0] == '\n')
            continue;
        
        char key[64], value[64];
        if (sscanf(line, "%63[^=]=%63s", key, value) == 2) {
            char *trimmed_key = trim_whitespace(key);
            char *trimmed_value = trim_whitespace(value);
            
            if (strcmp(trimmed_key, "THRESHOLD") == 0) {
                threshold = atoi(trimmed_value);
                if (threshold < 1 || threshold > 99)
                    threshold = DEFAULT_THRESHOLD;
            } else if (strcmp(trimmed_key, "INTERVAL") == 0) {
                interval = atoi(trimmed_value);
                if (interval < 1 || interval > 600)
                    interval = DEFAULT_INTERVAL;
            }
        }
    }
    
    fclose(fp);
    syslog(LOG_INFO, "Configuration loaded: threshold=%d%%, interval=%ds", threshold, interval);
}

int main(int argc, char *argv[]) {
    (void)argc;
    (void)argv;
    
    openlog("power-profiled", LOG_PID, LOG_DAEMON);
    
    signal(SIGTERM, signal_handler);
    signal(SIGINT, signal_handler);
    
    load_config();
    
    syslog(LOG_INFO, "Power Profile Manager daemon started");
    
    while (running) {
        int level = get_battery_level();
        int on_ac = is_on_ac();
        
        if (on_ac || level > threshold) {
            char *state = get_current_state();
            if (state && strcmp(state, "powersave") == 0) {
                apply_balanced();
            }
            clear_state();
        } else {
            char *state = get_current_state();
            if (!state || strcmp(state, "powersave") != 0) {
                apply_powersave();
                set_state("powersave");
            }
        }
        
        sleep(interval);
    }
    
    syslog(LOG_INFO, "Power Profile Manager daemon stopped");
    closelog();
    
    return 0;
}
