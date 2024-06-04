import wx
import os
import squarer_gui
import concurrent.futures
from PIL import Image, ImageFilter
from pathlib import Path
import subprocess

SIZE = 2400


class SquarerFrame(squarer_gui.MyFrame):
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.config = wx.Config("Squarer")

        self.executor = concurrent.futures.ThreadPoolExecutor()
        self.done_counter = 0
        self.todo_counter = 0
        self.single_output_path = None

        # Single Tab Controls
        self.single_go_button.Bind(wx.EVT_BUTTON, self.on_single_go)

        # Batch Tab Controls
        self.go_button.Bind(wx.EVT_BUTTON, self.on_go)
        self.input_dir_picker.Bind(wx.EVT_DIRPICKER_CHANGED, self.on_input_change)
        self.output_dir_picker.Bind(wx.EVT_DIRPICKER_CHANGED, self.on_output_change)
        self.input_dir_picker.SetPath(self.config.Read("input_dir_path", ""))
        self.output_dir_picker.SetPath(self.config.Read("output_dir_path", ""))

        self.show_single_file_button.Bind(wx.EVT_BUTTON, self.on_show_single_file)
        self.show_folder_button.Bind(wx.EVT_BUTTON, self.on_show_output_folder)

    def on_input_change(self, event):
        print("on input change")
        self.config.Write("input_dir_path", self.input_dir_picker.GetPath())

    def on_output_change(self, event):
        print("on output change")
        self.config.Write("output_dir_path", self.output_dir_picker.GetPath())

    def on_show_single_file(self, event):
        subprocess.Popen(fr'explorer /select,"{self.single_output_path}"')

    def on_show_output_folder(self, event):
        os.startfile(self.output_dir_picker.GetPath())

    def on_radio_change(self, event):
        pass

    def on_go(self, event):
        self.statusbar.SetStatusText("Processing...")
        input_dir = self.input_dir_picker.GetPath()
        output_dir = self.output_dir_picker.GetPath()
        self.done_counter = 0

        # List input images
        if os.path.isdir(input_dir):
            input_images = [os.path.join(input_dir, file) for file in os.listdir(input_dir) if
                            file.endswith(('.png', '.jpg', '.jpeg'))]
        else:
            input_images = [input_dir]

        # Create output dir if needed
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        self.todo_counter = len(input_images)
        for image_path in input_images:
            # self.process_image(image_path,  get_save_path(image_path, output_dir))
            future = self.executor.submit(self.process_image, image_path, get_save_path(image_path, output_dir))
            future.add_done_callback(self.UpdateStatus)

    def on_single_go(self, event):

        input_path = self.input_file_picker.GetPath()
        default_filename = Path(input_path).name
        wildcard = "JPEG Files (*.jpg)|*.jpg|PNG Files (*.png)|*.png"
        with wx.FileDialog(self, "Save File", wildcard=wildcard,
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT, defaultFile=default_filename) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # The user canceled the dialog

            # Get the path to the selected file
            output_path = fileDialog.GetPath()
            self.single_output_path = output_path

            # Check if the selected file has a valid extension
            ext = Path(output_path).suffix
            if ext.lower() not in [".jpg", ".png"]:
                wx.MessageBox("Please select a JPG or PNG file.", "Invalid File Type", wx.OK | wx.ICON_ERROR)
                return

            self.statusbar.SetStatusText("Processing...")
            # self.process_image(input_path, output_path)
            future = self.executor.submit(self.process_image, input_path, output_path)
            future.add_done_callback(self.UpdateSingleStatus)

    def UpdateStatus(self, future):
        self.done_counter = self.done_counter + 1
        self.statusbar.SetStatusText(f"Processed {self.done_counter}/{self.todo_counter}")
        if self.done_counter == self.todo_counter:
            self.statusbar.SetStatusText("All images processed.")
            self.show_folder_button.Enable()

    def UpdateSingleStatus(self, future):
        self.statusbar.SetStatusText(f"Done.")
        self.show_single_file_button.Enable()

    def process_image(self, input_image, output_path):
        # Step 1: Scale image
        img = Image.open(input_image)
        img = resize_with_ratio(img, SIZE)

        # Step 2: Create background
        bg_size = int(SIZE * 1.7)
        bg = img.resize((bg_size, bg_size), Image.Resampling.BICUBIC)
        bg = bg.filter(ImageFilter.GaussianBlur(180))

        # Step 3: Overlay
        final_image = Image.new("RGB", (SIZE, SIZE))
        final_image.paste(bg, ((SIZE - bg.width) // 2, (SIZE - bg.height) // 2))
        final_image.paste(img, ((SIZE - img.width) // 2, 0))

        # Save processed image
        final_image.save(output_path)


def zoom_at(img, x, y, zoom):
    w, h = img.size
    zoom2 = zoom * 2
    img = img.crop((x - w / zoom2, y - h / zoom2,
                    x + w / zoom2, y + h / zoom2))
    return img.resize((w, h), Image.Resampling.BICUBIC)


def resize_with_ratio(img, SIZE):
    w, h = img.size
    new_size = (SIZE * w // h, SIZE)
    return img.resize(new_size, Image.Resampling.BICUBIC)


def get_save_path(input_image, output_path):
    return os.path.join(output_path, os.path.basename(input_image))


class SquarerApp(wx.App):
    def OnInit(self):
        self.frame = SquarerFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True


if __name__ == "__main__":
    app = SquarerApp(0)
    app.MainLoop()
