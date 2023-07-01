import subprocess


def initialCheck():
    #
    tui_root_login = 0

    # Check for root subprocess (return a string)
    root_check = subprocess.run(["id", "-u"], capture_output=True, text=True).stdout.strip()

    # Check for root subprocess
    sudo_check = subprocess.run(["sudo", "-n", "true"], capture_output=True).returncode

    # Check for root access or if password is cached (if cache timestamp has not expired yet)
    try:
        if root_check == "0" or sudo_check == 0:
            return 0
        else:
            print("[ NOTICE! ] -> Please, run me as root!")
            password = input(" [ Trusted ] -> Specify the root password:")

            if subprocess.run(["sudo", "-S", "true"], input=password, capture_output=True, text=True).returncode == 0:
                return 0
            else:
                time.sleep(3)
                print("[ ERROR!! ] -> Incorrect password!")
                return 1
    except subprocess.CalledProcessError as error:
        print(error.output)
