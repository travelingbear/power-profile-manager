#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <ctype.h>

#define BATTERY_PATH "/sys/class/power_supply/BAT0"
#define STATE_FILE "/var/run/power-profile-state"
#define CONFIG_FILE "/etc/power-profiled.conf"

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

int get_turbo_status() {
    int turbo;
    
    // Intel: no_turbo (inverted: 0=enabled, 1=disabled)
    turbo = read_int_from_file("/sys/devices/system/cpu/intel_pstate/no_turbo");
    if (turbo >= 0) {
        return turbo == 0 ? 1 : 0;  // Return 1 for enabled, 0 for disabled
    }
    
    // AMD/Other: boost (normal: 1=enabled, 0=disabled)
    turbo = read_int_from_file("/sys/devices/system/cpu/cpufreq/boost");
    if (turbo >= 0) {
        return turbo;
    }
    
    return -1;  // Not available
}

void show_status() {
    char path[256], status[32], epp[32], platform[32], state[32];
    int level, turbo;
    
    snprintf(path, sizeof(path), "%s/capacity", BATTERY_PATH);
    level = read_int_from_file(path);
    
    snprintf(path, sizeof(path), "%s/status", BATTERY_PATH);
    if (read_string_from_file(path, status, sizeof(status)) < 0) {
        strcpy(status, "unknown");
    }
    
    if (read_string_from_file("/sys/devices/system/cpu/cpu0/cpufreq/energy_performance_preference", 
                             epp, sizeof(epp)) < 0) {
        strcpy(epp, "N/A");
    }
    
    turbo = get_turbo_status();
    
    if (read_string_from_file("/sys/firmware/acpi/platform_profile", platform, sizeof(platform)) < 0) {
        strcpy(platform, "N/A");
    }
    
    if (read_string_from_file(STATE_FILE, state, sizeof(state)) < 0) {
        strcpy(state, "inactive");
    }
    
    printf("Power Profile Manager Status\n");
    printf("=============================\n");
    
    if (level >= 0) {
        printf("Battery:          %d%%\n", level);
    } else {
        printf("Battery:          N/A\n");
    }
    
    printf("Power Status:     %s\n", status);
    printf("Active Profile:   %s\n", state);
    printf("\nCPU Settings:\n");
    printf("  EPP:            %s\n", epp);
    
    if (turbo >= 0) {
        printf("  Turbo Boost:    %s\n", turbo ? "enabled" : "disabled");
    } else {
        printf("  Turbo Boost:    N/A\n");
    }
    
    printf("  Platform:       %s\n", platform);
}

void monitor() {
    printf("Monitoring power profile (Ctrl+C to stop)...\n\n");
    while (1) {
        printf("\033[2J\033[H"); // Clear screen
        show_status();
        sleep(2);
    }
}

char* trim_whitespace(char *str) {
    char *end;
    
    // Trim leading space
    while(isspace((unsigned char)*str)) str++;
    
    if(*str == 0) return str;
    
    // Trim trailing space
    end = str + strlen(str) - 1;
    while(end > str && isspace((unsigned char)*end)) end--;
    
    end[1] = '\0';
    return str;
}

void show_config() {
    FILE *fp = fopen(CONFIG_FILE, "r");
    if (!fp) {
        printf("No configuration file found at %s\n", CONFIG_FILE);
        return;
    }
    
    printf("Configuration (%s):\n", CONFIG_FILE);
    printf("===================================\n");
    
    char line[256];
    while (fgets(line, sizeof(line), fp)) {
        if (line[0] != '#' && line[0] != '\n') {
            char *trimmed = trim_whitespace(line);
            if (strlen(trimmed) > 0) {
                printf("%s\n", trimmed);
            }
        }
    }
    fclose(fp);
}

void show_help() {
    printf("Usage: power-profile-ctl [COMMAND]\n\n");
    printf("Commands:\n");
    printf("  status     Show current power profile status (default)\n");
    printf("  monitor    Live monitoring of power profile\n");
    printf("  config     Show current configuration\n");
    printf("  help       Show this help message\n");
}

int main(int argc, char *argv[]) {
    if (argc < 2 || strcmp(argv[1], "status") == 0) {
        show_status();
    } else if (strcmp(argv[1], "monitor") == 0) {
        monitor();
    } else if (strcmp(argv[1], "config") == 0) {
        show_config();
    } else if (strcmp(argv[1], "help") == 0) {
        show_help();
    } else {
        printf("Unknown command: %s\n", argv[1]);
        show_help();
        return 1;
    }
    
    return 0;
}
