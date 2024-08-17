from tkinter import *
from tkinter import filedialog, messagebox, simpledialog
from PIL import ImageTk, Image
import os
import pickle

class IMG_Stegno:
    output_image_size = 0
    password_file = 'password.pkl'

    def __init__(self):
        
        # Load the password if it exists
        self.password = self.load_password()

    def load_password(self):

        # Attempt to load the password from a file
        try:
            with open(self.password_file, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:

            # Return None if file not found
            return None

    def save_password(self, password):

        # Save the given password to a file
        with open(self.password_file, 'wb') as f:
            pickle.dump(password, f)

    def main(self, root):

        # Set up the main window
        root.title('Image Steganography')
        root.geometry('500x600')
        root.resizable(width=False, height=False)
        root.config(bg='#e3f4f1')
        frame = Frame(root, bg='#e3f4f1')
        frame.grid()

        # Title label
        title = Label(frame, text='Image Steganography', font=('Times new roman', 25, 'bold'), bg='#e3f4f1')
        title.grid(pady=10, row=1)

        # Buttons to encode or decode
        encode = Button(frame, text="Encode", command=lambda: self.encode_frame1(frame), padx=14, font=('Helvetica', 14), bg='#e8c1c7')
        encode.grid(row=2)
        
        decode = Button(frame, text="Decode", command=lambda: self.decode_frame1(frame), padx=14, font=('Helvetica', 14), bg='#e8c1c7')
        decode.grid(pady=12, row=3)

        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1)

    def back(self, frame):

        # Go back to the main window
        frame.destroy()
        self.main(root)

    def encode_frame1(self, F):

        # Frame for selecting image to encode text
        F.destroy()
        F2 = Frame(root, bg='#e3f4f1')
        label1 = Label(F2, text='Select the Image in which \nyou want to hide text:', font=('Times new roman', 25, 'bold'), bg='#e3f4f1')
        label1.grid()

        # Button to select image
        button_bws = Button(F2, text='Select', command=lambda: self.encode_frame2(F2), font=('Helvetica', 18), bg='#e8c1c7')
        button_bws.grid()

        # Button to cancel and go back
        button_back = Button(F2, text='Cancel', command=lambda: self.back(F2), font=('Helvetica', 18), bg='#e8c1c7')
        button_back.grid(pady=15)
        F2.grid()

    def decode_frame1(self, F):

        # Frame for selecting image to decode text
        F.destroy()
        d_f2 = Frame(root, bg='#e3f4f1')
        label1 = Label(d_f2, text='Select Image with Hidden text:', font=('Times new roman', 25, 'bold'), bg='#e3f4f1')
        label1.grid()
        
        # Button to select image
        button_bws = Button(d_f2, text='Select', command=lambda: self.decode_frame2(d_f2), font=('Helvetica', 18), bg='#e8c1c7')
        button_bws.grid()

        # Button to cancel and go back
        button_back = Button(d_f2, text='Cancel', command=lambda: self.back(d_f2), font=('Helvetica', 18), bg='#e8c1c7')
        button_back.grid(pady=15)
        d_f2.grid()

    def encode_frame2(self, e_F2):

        # Open file dialog to select an image for encoding
        myfile = filedialog.askopenfilename(filetypes=[('png', '.png'), ('jpeg', '.jpeg'), ('jpg', '.jpg'), ('All Files', '.*')])

        if not myfile:
            messagebox.showerror("Error", "You have selected nothing!")

        else:

            # Display selected image and prompt for text input
            e_F2.destroy()
            e_pg = Frame(root, bg='#e3f4f1')
            my_img = Image.open(myfile)
            new_image = my_img.resize((300, 200))
            img = ImageTk.PhotoImage(new_image)

            label3 = Label(e_pg, text='Selected Image', font=('Helvetica', 14, 'bold'))
            label3.grid()
            board = Label(e_pg, image=img)
            board.image = img
            self.output_image_size = os.stat(myfile)
            self.o_image_w, self.o_image_h = my_img.size
            board.grid()

            label2 = Label(e_pg, text='Enter the message', font=('Helvetica', 14, 'bold'))
            label2.grid(pady=15)
            text_a = Text(e_pg, width=50, height=10)
            text_a.grid()

            # Buttons to cancel or encode
            button_back = Button(e_pg, text='Cancel', command=lambda: self.back(e_pg), font=('Helvetica', 14), bg='#e8c1c7')
            button_back.grid(pady=15)
            encode_button = Button(e_pg, text='Encode', command=lambda: [self.enc_fun(text_a, my_img), self.back(e_pg)], font=('Helvetica', 14), bg='#e8c1c7')
            encode_button.grid(pady=15)
            e_pg.grid(row=1)

    def decode_frame2(self, d_F2):

        # Open file dialog to select an image for decoding
        myfiles = filedialog.askopenfilename(filetypes=[('png', '.png'), ('jpeg', '.jpeg'), ('jpg', '.jpg'), ('All Files', '.*')])
        if not myfiles:
            messagebox.showerror("Error", "You have selected nothing!")
            return

        d_F2.destroy()
        d_F3 = Frame(root, bg='#e3f4f1')
        my_img = Image.open(myfiles, 'r')
        decoded_message = self.decode(my_img)

        # Display selected image and decoded message
        my_image = my_img.resize((300, 200))
        img = ImageTk.PhotoImage(my_image)
        label4 = Label(d_F3, text='Selected Image:', font=('Helvetica', 14, 'bold'))
        label4.grid()
        board = Label(d_F3, image=img)
        board.image = img
        board.grid()

        label_decoded = Label(d_F3, text='Decoded Message:', font=('Helvetica', 14, 'bold'))
        label_decoded.grid(pady=15)

        text_decoded = Text(d_F3, width=50, height=10)
        text_decoded.insert('1.0', decoded_message)
        text_decoded.config(state='disabled')
        text_decoded.grid()

        # Button to go back
        button_back = Button(d_F3, text='Cancel', command=lambda: self.frame_3(d_F3), font=('Helvetica', 14), bg='#e8c1c7')
        button_back.grid(pady=15)
        d_F3.grid(row=1)

    def decode(self, image):

        # Decode text from the image if password is set
        if self.password is None:
            messagebox.showerror("Error", "No password set for decoding!")
            return

        entered_password = simpledialog.askstring("Password", "Enter the password:", show='*')
        if entered_password != self.password:
            messagebox.showerror("Error", "Incorrect password!")
            return

        image_data = iter(image.getdata())
        data = b''

        # Extract hidden text from image
        while True:
            pixels = [value for value in next(image_data)[:3] +
                      next(image_data)[:3] +
                      next(image_data)[:3]]
            binary_str = ''
            for i in pixels[:8]:
                binary_str += '0' if i % 2 == 0 else '1'

            data += bytes([int(binary_str, 2)])
            if pixels[-1] % 2 != 0:
                return data.decode('utf-8')

    def generate_Data(self, data):

        # Convert text data to binary format
        new_data = [format(ord(i), '08b') for i in data]
        return new_data

    def modify_Pix(self, pix, data):

        # Modify image pixels to hide data
        dataList = self.generate_Data(data)
        dataLen = len(dataList)
        imgData = iter(pix)
        for i in range(dataLen):
            pix = [value for value in next(imgData)[:3] +
                   next(imgData)[:3] +
                   next(imgData)[:3]]

            for j in range(8):
                if (dataList[i][j] == '0') and (pix[j] % 2 != 0):
                    pix[j] -= 1
                elif (dataList[i][j] == '1') and (pix[j] % 2 == 0):
                    pix[j] -= 1

            # Adjust the least significant bit of the last pixel
            if (i == dataLen - 1):
                if (pix[-1] % 2 == 0):
                    pix[-1] -= 1
            else:
                if (pix[-1] % 2 != 0):
                    pix[-1] -= 1

            pix = tuple(pix)
            yield pix[0:3]
            yield pix[3:6]
            yield pix[6:9]

    def encode_enc(self, newImg, data):

        # Encode the data into the image
        w = newImg.size[0]
        (x, y) = (0, 0)

        for pixel in self.modify_Pix(newImg.getdata(), data):
            newImg.putpixel((x, y), pixel)
            if (x == w - 1):
                x = 0
                y += 1
            else:
                x += 1

    def enc_fun(self, text_a, myImg):

        # Handle encoding process
        self.password = simpledialog.askstring("Password", "Set a password for encoding:", show='*')
        if self.password is None:
            return

        data = text_a.get("1.0", "end-1c")
        if len(data) == 0:
            messagebox.showinfo("Alert", "Kindly enter text in TextBox")
        else:
            self.save_password(self.password)
            newImg = myImg.copy()
            self.encode_enc(newImg, data)
            temp = os.path.splitext(os.path.basename(myImg.filename))[0]
            newImg.save(filedialog.asksaveasfilename(initialfile=temp, filetypes=[('png', '*.png')], defaultextension=".png"))
            messagebox.showinfo("Success", "Encoding Successful\nFile is saved as Image_with_hiddentext.png in the same directory")

    def frame_3(self, frame):

        # Go back to the main window
        frame.destroy()
        self.main(root)

# Create the main window and start the application
root = Tk()
o = IMG_Stegno()
o.main(root)
root.mainloop()
