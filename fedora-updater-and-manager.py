import subprocess
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

# Start message to show in log area
start_info = """
    sysUpdate v1.0 (by piotrek)

    Use this software to perform a full update in Fedora System.

    Options to choose from:
    - DNF                 Run 'sudo dnf -y upgrade --refresh'
    - Flatpak             Run 'flatpak -y update'
    - Firmware            Run 'sudo fwupdmgr refresh --force'
                          Run 'sudo fwupdmgr get-updates'
                          Run 'sudo fwupdmgr update'
    """


# Get updates options and run
def run_update(button):
    has_command = 0
    update_command = []

    if dnf_checkbox.get_active():
        has_command += 1
        command_dnf = "ls -lha"

        dnf_result = subprocess.Popen(command_dnf, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                      universal_newlines=True)

        subprocess.Popen("ls -lha", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                      universal_newlines=True)

        log_area.get_buffer().set_text("Proceeding DNF -y update...\n\n")

        for line in dnf_result.stdout:
            # Insere a saída na área de texto
            log_area.get_buffer().insert_at_cursor(line)
            # Atualiza a interface gráfica
            while Gtk.events_pending():
                Gtk.main_iteration()

    if flatpak_checkbox.get_active():
        has_command += 1
        command_flatpak = "flatpak -y update"

        # Run flatpak update and show verbose in log area
        flatpak_result = subprocess.Popen(command_flatpak, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                          universal_newlines=True)

        # Clear log area and insert update info
        log_area.get_buffer().set_text("Proceeding flatpak -y update...\n\n")

        for line in flatpak_result.stdout:
            # Insert log return to log area
            log_area.get_buffer().insert_at_cursor(line)
            # Update graphical interface
            while Gtk.events_pending():
                Gtk.main_iteration()

    if firmware_checkbox.get_active():
        has_command += 1
        update_command.append("sudo fwupdmgr refresh --force")
        update_command.append("sudo fwupdmgr get-updates")
        update_command.append("sudo fwupdmgr update")

    if has_command == 0:
        dialog = Gtk.MessageDialog(parent=main_window, flags=0, message_type=Gtk.MessageType.WARNING,
                                   buttons=Gtk.ButtonsType.OK, text="Nenhum serviço selecionado")
        dialog.run()
        dialog.destroy()
        return

    command = " && ".join(update_command)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        dialog = Gtk.MessageDialog(parent=main_window, flags=0, message_type=Gtk.MessageType.INFO,
                                   buttons=Gtk.ButtonsType.OK, text="Atualização concluída")
        dialog.run()
        dialog.destroy()
    else:
        dialog = Gtk.MessageDialog(parent=main_window, flags=0, message_type=Gtk.MessageType.ERROR,
                                   buttons=Gtk.ButtonsType.OK, text="Erro de atualização")
        dialog.run()
        dialog.destroy()


# Exit applications
def exit_application(button):
    Gtk.main_quit()


# Main window creation
main_window = Gtk.Window()
main_window.set_title("sysUpdate v1.0 (by piotrek)")
main_window.set_default_size(640, 480)
main_window.connect("destroy", Gtk.main_quit)

# Checkboxes control variables
dnf_checkbox = Gtk.CheckButton(label="DNF")
flatpak_checkbox = Gtk.CheckButton(label="Flatpak")
firmware_checkbox = Gtk.CheckButton(label="Firmware")

# Main window label
title_label = Gtk.Label(label="Choose the options and click in update button: ")
title_label.set_hexpand(True)

# Main window update button
update_button = Gtk.Button(label="Update")
update_button.set_hexpand(True)

# Main window log area
log_area = Gtk.TextView()
log_area.set_editable(False)
log_area.set_hexpand(False)  # Impede a expansão horizontal
log_area.set_vexpand(False)  # Impede a expansão vertical
log_area.get_buffer().set_text(start_info)

# Main window exit button
exit_button = Gtk.Button(label="Exit")
exit_button.set_hexpand(True)

# Grid layout for main window
grid = Gtk.Grid()
grid.set_column_spacing(5)
grid.set_row_spacing(5)
main_window.add(grid)

# Add elements to the grid
grid.attach(title_label, 0, 0, 3, 1)
grid.attach(dnf_checkbox, 0, 1, 1, 1)
grid.attach(flatpak_checkbox, 1, 1, 1, 1)
grid.attach(firmware_checkbox, 2, 1, 1, 1)
grid.attach(update_button, 0, 2, 3, 1)
grid.attach(log_area, 0, 3, 3, 1)
grid.attach(exit_button, 0, 4, 3, 1)

# Run update function when update button is clicked
update_button.connect("clicked", run_update)

# Run exit_application function when exit button is clicked
exit_button.connect("clicked", exit_application)

# Show all elements
main_window.show_all()

# Start Gtk main loop
Gtk.main()