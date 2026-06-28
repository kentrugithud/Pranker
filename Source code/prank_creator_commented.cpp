// ==========================================
// Подробно прокомментированная версия
// ==========================================

#include <iostream>
#include <fstream>
#include <string>
#include <filesystem>

namespace fs = std::filesystem;

// Класс, отвечающий за генерацию BAT-файлов.
class PrankCreator {
public:
    // 1. Система (Выключение, Рестарт, Сон)
    // Создает BAT-файл выключения/перезагрузки/сна.
    bool createShutdownBat(const std::string& filename, const std::string& action, int delay) {
        std::ofstream file(filename);
        if (!file.is_open()) return false;

        file << "@echo off\n";
        if (delay > 0) {
            file << "timeout /t " << delay << " /nobreak >nul\n";
        }

        if (action == "shutdown") {
            file << "shutdown /s /f /t 0\n";
        } else if (action == "restart") {
            file << "shutdown /r /f /t 0\n";
        } else if (action == "sleep") {
            file << "rundll32.exe powrprof.dll,SetSuspendState 0,1,0\n";
        }

        file << "exit\n";
        file.close();
        return true;
    }

    // 2. YouTube пранк
    // Создает BAT-файл для открытия ссылки YouTube.
    bool createYoutubeBat(const std::string& filename, const std::string& url, int count, int delay) {
        std::ofstream file(filename);
        if (!file.is_open()) return false;

        file << "@echo off\n";
        if (delay > 0) {
            file << "timeout /t " << delay << " /nobreak >nul\n";
        }

        file << "for /L %%i in (1,1," << count << ") do (\n";
        file << "  start \"\" \"" << url << "\"\n";
        file << ")\n";

        file << "exit\n";
        file.close();
        return true;
    }

    // 3. Закрытие всех пользовательских программ
    // Создает BAT-файл закрытия пользовательских процессов.
    bool createCloseAppsBat(const std::string& filename, int delay) {
        std::ofstream file(filename);
        if (!file.is_open()) return false;

        file << "@echo off\n";
        if (delay > 0) {
            file << "timeout /t " << delay << " /nobreak >nul\n";
        }
        
        // Принудительно завершает процессы текущего пользователя, сохраняя проводник и консоль
        file << "taskkill /F /FI \"STATUS eq RUNNING\" /FI \"USERNAME eq %USERNAME%\" /IM * /T /FI \"IMAGENAME ne explorer.exe\" /FI \"IMAGENAME ne cmd.exe\" >nul 2>&1\n";
        file << "exit\n";
        
        file.close();
        return true;
    }
};

// Точка входа программы.
// Получает параметры командной строки и вызывает нужный генератор.
int main(int argc, char* argv[]) {
    if (argc < 5) return 1;

    std::string prank_type = argv[1];
    int delay = std::stoi(argv[2]);
    std::string filename = argv[3];
    std::string save_path = argv[4];

    fs::path full_path = fs::path(save_path) / filename;

    PrankCreator creator;
    bool success = false;

    if (prank_type == "shutdown") {
        if (argc < 6) return 1;
        success = creator.createShutdownBat(full_path.string(), argv[5], delay);
    } else if (prank_type == "youtube") {
        if (argc < 7) return 1;
        success = creator.createYoutubeBat(full_path.string(), argv[5], std::stoi(argv[6]), delay);
    } else if (prank_type == "close_apps") {
        success = creator.createCloseAppsBat(full_path.string(), delay);
    }

    return success ? 0 : 1;
}