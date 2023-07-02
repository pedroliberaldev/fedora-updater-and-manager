import subprocess
import getpass
import time


# Check for root privileges and ask for the password if necessary
def check_for_root():
    # Check for root subprocess (return a string)
    root_check = subprocess.run(["id", "-u"], capture_output=True, text=True).stdout.strip()

    # Check for root subprocess
    sudo_check = subprocess.run(["sudo", "-n", "true"], capture_output=True).returncode

    # Check for root access or if password is cached (if cache timestamp has not expired yet)
    try:
        # Check for root user or privileges by sudo
        if root_check == "0" or sudo_check == 0:
            return 0
        else:
            print("[ NOTICE! ] -> Please, run me as root!")
            password = getpass.getpass("[ Trusted ] -> Specify the root password:")

            if subprocess.run(["sudo", "-S", "true"], input=password, capture_output=True, text=True).returncode != 0:
                time.sleep(3)
                print("[ ERROR!! ] -> Incorrect password!")
                return 1
    except subprocess.CalledProcessError as error:
        print(error.output)
    else:
        return 0


# Perform a packages update
def check_dnf_updates():
    try:
        print("=> Proceeding sudo dnf -y upgrade --refresh...")

        # Try to execute user-selected packages installation
        dnf_execution = subprocess.Popen(["sudo", "dnf", "-y", "upgrade", "--refresh"], stdout=subprocess.PIPE,
                                         universal_newlines=True)

        for output in dnf_execution.stdout:
            print(output, end='')

        dnf_execution.wait()  # Wait for the subprocess to finish

        # Try to execute user-selected packages installation
        if dnf_execution.returncode == 0:
            print(">>>   All packages are up to date!   <<<")
            return 0
        else:
            print(">>>   ERROR: System update failed   <<<")
            return 1
    except subprocess.CalledProcessError as error:
        print(error.output)


def check_flatpak_updates():
    try:
        print("=> Proceeding flatpak -y update...")

        # Try to execute user-selected packages installation
        flatpak_execution = subprocess.Popen(["flatpak", "-y", "update"], stdout=subprocess.PIPE,
                                             universal_newlines=True)

        for output in flatpak_execution.stdout:
            print(output, end='')

        flatpak_execution.wait()  # Wait for the subprocess to finish

        # Try to execute user-selected packages installation
        if flatpak_execution.returncode == 0:
            print(">>>   All packages are up to date!   <<<")
            return 0
        else:
            print(">>>   ERROR: System update failed   <<<")
            return 1
    except subprocess.CalledProcessError as error:
        print(error.output)


def check_firmware_updates():
    try:
        print("=> Proceeding firmware upgrade commands...")

        print("  * sudo fwupdmgr refresh --force...")
        # Try to ...
        firmware_refresh_execution = subprocess.Popen(["sudo", "fwupdmgr", "-y", "--force"], stdout=subprocess.PIPE,
                                                      universal_newlines=True)

        for output in firmware_refresh_execution.stdout:
            print(output, end='')

        firmware_refresh_execution.wait()  # Wait for the subprocess to finish

        print("  * sudo fwupdmgr get-updates...")
        # Try to ...
        firmware_get_updates_execution = subprocess.Popen(["sudo", "fwupdmgr", "get-updates"], stdout=subprocess.PIPE,
                                                          universal_newlines=True)

        for output in firmware_get_updates_execution.stdout:
            print(output, end='')

        firmware_get_updates_execution.wait()  # Wait for the subprocess to finish

        print("  * sudo fwupdmgr update...")
        # Try to ...
        firmware_update_execution = subprocess.Popen(["sudo", "fwupdmgr", "update"], stdout=subprocess.PIPE,
                                                     universal_newlines=True)

        for output in firmware_update_execution.stdout:
            print(output, end='')

        firmware_update_execution.wait()  # Wait for the subprocess to finish

        # Try to execute user-selected packages installation
        if firmware_refresh_execution.returncode == 0 and firmware_get_updates_execution.returncode == 0 and \
                firmware_update_execution.returncode == 0:
            print(">>>   All packages are up to date!   <<<")
            return 0
        else:
            print(">>>   ERROR: System update failed   <<<")
            return 1
    except subprocess.CalledProcessError as error:
        print(error.output)


def check_updates():
    print("Checking for root privileges...")
    check_for_root()

    print("Checking for package updates...")
    check_dnf_updates()
    check_flatpak_updates()
    check_firmware_updates()


check_updates()
