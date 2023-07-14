import subprocess
import getpass
import time


# Check for root privileges and ask for the password if necessary
def check_for_root():
    # Check if the program is running as root
    root_check = subprocess.run(["id", "-u"], capture_output=True, text=True).stdout.strip()

    # Check for sudo root privileges
    sudo_check = subprocess.run(["sudo", "-n", "true"], capture_output=True).returncode

    # In case of the program is running as normal user, ask for the sudo password
    if not int(root_check) or not sudo_check:
        print("[ NOTICE ] -> Please, run me as root!")

        try:
            # Receive the sudo password
            password = getpass.getpass("[ Trusted ] -> Specify the root password:")
        except Exception as passError:
            print(f"[ ERROR!! ] -> {passError}")
        else:
            # Verify sudo root privileges after password entry and return 1 if unsuccessful
            if 0 != subprocess.run(["sudo", "-S", "true"], input=password, capture_output=True, text=True).returncode:
                time.sleep(3)
                print("[ ERROR!! ] -> Incorrect password!")
                return 1

    # In case of successful sudo password input, return 0
    return 0


# Perform a dnf packages update
def check_dnf_updates():
    try:
        print("=> Proceeding sudo dnf -y upgrade --refresh...")

        # Try to execute a dnf system update
        dnf_execution = subprocess.Popen(["sudo", "dnf", "-y", "upgrade", "--refresh"], stdout=subprocess.PIPE,
                                         universal_newlines=True)

        # Print each subprocess line return (real time output)
        for output in dnf_execution.stdout:
            print(output, end='')

        # Doesn't allow the program to continue before subprocess finish
        dnf_execution.wait()
    except subprocess.CalledProcessError as dnfError:
        print(f"[ ERROR!! ] -> {dnfError.output}")
        return 1
    else:
        # Verify if DNF update was successfully finished by return code
        if 0 != dnf_execution.returncode:
            print("[ ERROR!! ] -> DNF update failed!")
            return 1
        else:
            print("[ SUCCESS ] -> DNF update finished!")
            return 0


def check_flatpak_updates():
    try:
        print("=> Proceeding flatpak -y update...")

        # Try to execute a flatpak system update
        flatpak_execution = subprocess.Popen(["flatpak", "-y", "update"], stdout=subprocess.PIPE,
                                             universal_newlines=True)

        # Print each subprocess line return (real time output)
        for output in flatpak_execution.stdout:
            print(output, end='')

        # Doesn't allow the program to continue before subprocess finish
        flatpak_execution.wait()
    except subprocess.CalledProcessError as flatpakError:
        print(f"[ ERROR!! ] -> {flatpakError.output}")
        return 1
    else:
        # Verify if flatpak update was successfully finished by return code
        if 0 != flatpak_execution.returncode:
            print("[ ERROR!! ] -> Flatpak update failed!")
            return 1
        else:
            print("[ SUCCESS ] -> Flatpak update finished!")
            return 0


def check_firmware_updates():
    print("=> Proceeding firmware upgrade commands...")

    # Firmware refresh section
    try:
        print("   * sudo fwupdmgr refresh --force...")

        # Try to execute a firmware refresh
        firmware_refresh_execution = subprocess.Popen(["sudo", "fwupdmgr", "refresh", "--force"],
                                                      stdout=subprocess.PIPE,
                                                      universal_newlines=True)

        # Print each subprocess line return (real time output)
        for output_firmware_refresh in firmware_refresh_execution.stdout:
            print(output_firmware_refresh, end='')

            # Doesn't allow the program to continue before subprocess finish
            firmware_refresh_execution.wait()
    except subprocess.CalledProcessError as firmwareRefreshError:
        print(f"[ ERROR!! ] -> {firmwareRefreshError.output}")
        return 1
    else:
        # Firmware get updates section
        try:
            print("   * sudo fwupdmgr get-updates...")

            # Try to execute a firmware get updates
            firmware_get_updates_execution = subprocess.Popen(["sudo", "fwupdmgr", "get-updates"],
                                                              stdout=subprocess.PIPE,
                                                              universal_newlines=True)

            # Print each subprocess line return (real time output)
            for output_firmware_get_updates in firmware_get_updates_execution.stdout:
                print(output_firmware_get_updates, end='')

                # Doesn't allow the program to continue before subprocess finish
                firmware_get_updates_execution.wait()

        except subprocess.CalledProcessError as firmwareGetUpdatesError:
            print(f"[ ERROR!! ] -> {firmwareGetUpdatesError.output}")
            return 1
        else:
            # Firmware update section
            try:
                print("   * sudo fwupdmgr update...")

                # Try to execute a firmware get updates
                firmware_update_execution = subprocess.Popen(["sudo", "fwupdmgr", "update"],
                                                             stdout=subprocess.PIPE,
                                                             universal_newlines=True)

                # Print each subprocess line return (real time output)
                for output_firmware_update in firmware_update_execution.stdout:
                    print(output_firmware_update, end='')

                    # Doesn't allow the program to continue before subprocess finish
                    firmware_update_execution.wait()

            except subprocess.CalledProcessError as firmwareUpdateError:
                print(f"[ ERROR!! ] -> {firmwareUpdateError.output}")
                return 1
            else:
                # Verify if firmware update was successfully finished by return code for each step
                if 0 != firmware_refresh_execution.returncode or 0 != firmware_get_updates_execution.returncode \
                        or 0 != firmware_update_execution.returncode:
                    print("[ ERROR!! ] -> Firmware refresh failed!")
                    return 1
                else:
                    print("[ SUCCESS ] -> Firmware refresh finished!")
                    return 0


def check_updates():
    print("Checking for root privileges...")
    check_for_root()

    print("Checking for package updates...")
    check_dnf_updates()
    check_flatpak_updates()
    check_firmware_updates()


check_updates()
