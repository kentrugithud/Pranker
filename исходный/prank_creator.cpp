#include <iostream>
#include <fstream>
#include <string>

class PrankCreator {
public:
    bool createShutdownBat(const std::string& filename, const std::string& action, int delay) {
        std::ofstream file(filename);
        if (!file.is_open()) return false;

        std::string cmd, action_text, warning, final_msg;
        
        if (action == "shutdown") {
            cmd = "shutdown /s /f /t 3";
            action_text = "выключение";
            warning = "ВЫКЛЮЧЕНИЕ КОМПЬЮТЕРА";
            final_msg = "Компьютер будет выключен через 3 секунды...";
        } else if (action == "restart") {
            cmd = "shutdown /r /f /t 3";
            action_text = "перезагрузка";
            warning = "ПЕРЕЗАГРУЗКА СИСТЕМЫ";
            final_msg = "Компьютер будет перезагружен через 3 секунды...";
        } else {
            cmd = "rundll32.exe powrprof.dll,SetSuspendState 0,1,0";
            action_text = "спящий режим";
            warning = "ПЕРЕХОД В СПЯЩИЙ РЕЖИМ";
            final_msg = "Компьютер переходит в спящий режим...";
        }

        file << "@echo off\n";
        file << "chcp 1251 > nul\n";
        file << "title Системное уведомление Windows\n\n";
        file << "echo ========================================\n";
        file << "echo        СИСТЕМНОЕ УВЕДОМЛЕНИЕ\n";
        file << "echo ========================================\n";
        file << "echo.\n";
        file << "echo ВНИМАНИЕ: ИНИЦИИРОВАНО " << warning << "\n";
        file << "echo.\n";
        file << "echo Компьютер будет переведен в " << action_text << "\n";
        file << "echo через " << delay << " секунд!\n";
        file << "echo.\n";
        file << "echo Для отмены операции закройте это окно.\n";
        file << "echo ========================================\n\n";
        file << "timeout /t " << delay << " /nobreak > nul\n\n";
        file << "echo.\n";
        file << "echo " << final_msg << "\n";
        file << "echo.\n\n";
        file << cmd << "\n\n";
        file << "echo Операция завершена.\n";
        file << "echo PrankMaster Pro v1.3.5\n\n";
        file << "timeout /t 2 /nobreak > nul\n";

        file.close();
        return true;
    }

    bool createYoutubeBat(const std::string& filename, const std::string& url, int count, int delay) {
        std::ofstream file(filename);
        if (!file.is_open()) return false;

        file << "@echo off\n";
        file << "chcp 1251 > nul\n";
        file << "title Медиа проигрыватель\n\n";
        file << "echo ========================================\n";
        file << "echo    ЗАПУСК МЕДИА ПРОИГРЫВАТЕЛЯ\n";
        file << "echo ========================================\n";
        file << "echo.\n";
        file << "echo Подготовка к воспроизведению видео...\n";
        file << "echo Ожидание " << delay << " секунд...\n";
        file << "echo.\n";
        file << "echo Для отмены закройте это окно.\n";
        file << "echo ========================================\n\n";
        file << "timeout /t " << delay << " /nobreak > nul\n\n";
        file << "set COUNT=" << count << "\n";
        file << "set VIDEO_URL=" << url << "\n\n";
        file << "echo Запуск видео контента...\n";
        file << "echo Открытие %COUNT% медиа сессий...\n\n";
        file << "for /L %%i in (1,1,%COUNT%) do (\n";
        file << "    start \"\" \"iexplore.exe\" \"%VIDEO_URL%\"\n";
        file << "    timeout /t 1 /nobreak > nul\n";
        file << "    echo Сессия %%i/%COUNT% запущена...\n";
        file << ")\n\n";
        file << "echo.\n";
        file << "echo ========================================\n";
        file << "echo    ВОСПРОИЗВЕДЕНИЕ АКТИВИРОВАНО\n";
        file << "echo ========================================\n";
        file << "echo.\n";
        file << "echo Все медиа сессии успешно запущены!\n";
        file << "echo Наслаждайтесь просмотром!\n";
        file << "echo.\n";
        file << "echo PrankMaster Pro v1.3.5\n";
        file << "echo.\n\n";
        file << "timeout /t 3 /nobreak > nul\n";

        file.close();
        return true;
    }

    bool createFakeBsodBat(const std::string& filename, int delay) {
        std::ofstream file(filename);
        if (!file.is_open()) return false;

        file << "@echo off\n";
        file << "chcp 1251 > nul\n";
        file << "title System Process\n\n";
        file << "echo Поиск FakeBsod.exe...\n";
        file << "if exist \"FakeBsod.exe\" (\n";
        file << "    echo FakeBsod.exe найден в текущей папке\n";
        file << ") else (\n";
        file << "    echo ОШИБКА: FakeBsod.exe не найден!\n";
        file << "    echo Положите FakeBsod.exe в ту же папку что и этот BAT файл\n";
        file << "    pause\n";
        file << "    exit\n";
        file << ")\n\n";
        file << "echo Запуск через " << delay << " секунд...\n";
        file << "timeout /t " << delay << " /nobreak > nul\n\n";
        file << "echo Запуск FakeBsod.exe...\n";
        file << "start \"\" \"FakeBsod.exe\"\n\n";
        file << "exit\n";

        file.close();
        return true;
    }
};

int main(int argc, char* argv[]) {
    if (argc < 5) {
        std::cerr << "Использование: " << argv[0] << " <type> <delay> <filename> <save_path> [additional_args...]\n";
        return 1;
    }

    std::string prank_type = argv[1];
    int delay = std::stoi(argv[2]);
    std::string filename = argv[3];
    std::string save_path = argv[4];

    // Простой путь без filesystem
    std::string full_path = save_path + "\\" + filename;

    PrankCreator creator;
    bool success = false;

    if (prank_type == "shutdown") {
        if (argc < 6) {
            std::cerr << "Для shutdown пранка нужен тип действия\n";
            return 1;
        }
        std::string action = argv[5];
        success = creator.createShutdownBat(full_path, action, delay);
    } else if (prank_type == "youtube") {
        if (argc < 7) {
            std::cerr << "Для YouTube пранка нужны URL и количество\n";
            return 1;
        }
        std::string url = argv[5];
        int count = std::stoi(argv[6]);
        success = creator.createYoutubeBat(full_path, url, count, delay);
    } else if (prank_type == "fake_bsod") {
        success = creator.createFakeBsodBat(full_path, delay);
    } else {
        std::cerr << "Неизвестный тип пранка: " << prank_type << "\n";
        return 1;
    }

    if (success) {
        std::cout << "Пранк успешно создан: " << full_path << "\n";
        return 0;
    } else {
        std::cerr << "Ошибка создания файла: " << full_path << "\n";
        return 1;
    }
}