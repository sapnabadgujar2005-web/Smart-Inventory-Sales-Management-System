from tkinter import *
from tkinter.ttk import Treeview
from PIL import Image, ImageTk
from db_config import connect_db
from tkinter import messagebox
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

class LoginForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory System Login")
        self.root.geometry("1200x700")
        self.root.state("zoomed")

        # ================= BACKGROUND =================
        bg_img = Image.open("dash11.png")
        bg_img = bg_img.resize((1366, 768))
        self.bg_photo = ImageTk.PhotoImage(bg_img)

        Label(self.root, image=self.bg_photo).place(x=0, y=0, relwidth=1, relheight=1)

        # ================= MAIN FRAME =================
        frame = Frame(self.root, bg="#2e1065")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=900, height=500)

        # ================= LEFT IMAGE =================
        left_img = Image.open("left_side.png")
        left_img = left_img.resize((400, 400))
        self.left_photo = ImageTk.PhotoImage(left_img)

        Label(frame, image=self.left_photo, bg="#2e1065").place(x=20, y=50)

        # ================= RIGHT LOGIN =================
        Label(frame, text="Login",
              font=("Segoe UI", 22, "bold"),
              bg="#2e1065", fg="white").place(x=550, y=50)

        # USERNAME
        Label(frame, text="Username",
              bg="#2e1065", fg="#9ca3af").place(x=500, y=130)

        self.username = Entry(frame,
                              bg="#1f2937",
                              fg="white",
                              bd=0,
                              font=("Segoe UI", 11))
        self.username.place(x=500, y=160, width=250, height=30)

        # PASSWORD
        Label(frame, text="Password",
              bg="#2e1065", fg="#9ca3af").place(x=500, y=210)

        self.password = Entry(frame,
                              bg="#1f2937",
                              fg="white",
                              bd=0,
                              show="*",
                              font=("Segoe UI", 11))
        self.password.place(x=500, y=240, width=250, height=30)

        # SHOW / HIDE BUTTON
        self.show_img = ImageTk.PhotoImage(Image.open("SHOW.jpeg").resize((20, 30)))
        self.hide_img = ImageTk.PhotoImage(Image.open("hide.png").resize((20, 30)))

        self.show_btn = Button(frame,
                               image=self.show_img,
                               bd=0,
                               bg="#1f2937",
                               cursor="hand2",
                               command=self.toggle_password)
        self.show_btn.place(x=760, y=240)

        self.showing = False

        # LOGIN BUTTON
        Button(frame,
               text="LOGIN",
               bg="#2563eb",
               fg="white",
               font=("Segoe UI", 11, "bold"),
               bd=0,
               width=20,
               command=self.login).place(x=500, y=300)

        # FORGOT PASSWORD
        Button(frame,
               text="Forgot Password?",
               bg="#2e1065",
               fg="#60a5fa",
               bd=0,
               cursor="hand2",
               command=self.forgot_window).place(x=500, y=350)

        # SIGN UP
        Label(frame,
              text="Don't have an account?",
              bg="#2e1065",
              fg="white").place(x=500, y=390)

        Button(frame,
               text="Sign Up",
               bg="#16a34a",
               fg="white",
               bd=0,
               cursor="hand2",
               command=self.signup_window).place(x=680, y=385)



    def set_background(self, win, img_path, width=1366, height=768):
        from PIL import Image, ImageTk

        img = Image.open(img_path)
        img = img.resize((width, height), Image.LANCZOS)

        bg = ImageTk.PhotoImage(img)

        bg_label = Label(win, image=bg)
        bg_label.image = bg   # prevent garbage collection
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        bg_label.lower()  # send to back

    # ================= LOGIN =================
    def login(self):
        user = self.username.get()
        pwd = self.password.get()

        if user == "" or pwd == "":
            messagebox.showerror("Error", "All fields required")
            return

        # ✅ If using database, keep your DB code here
        # For now simple success:
        messagebox.showinfo("Success", f"Welcome {user}")

        # 👉 IMPORTANT: Open dashboard
        self.open_dashboard()
        # ================= TOGGLE PASSWORD =================
    def toggle_password(self):
        if self.showing:
            self.password.config(show="*")
            self.show_btn.config(image=self.show_img)
            self.showing = False
        else:
            self.password.config(show="")
            self.show_btn.config(image=self.hide_img)
            self.showing = True

    # ================= FORGOT PASSWORD =================
    def forgot_window(self):
        win = Toplevel(self.root)
        self.set_background(win, "dash11.png")
        win.title("Forgot Password")
        win.geometry("350x250")

        Label(win, text="Reset Password", font=("Segoe UI", 14, "bold")).pack(pady=10)

        Label(win, text="Username").pack()
        user = Entry(win)
        user.pack(pady=5)

        Label(win, text="New Password").pack()
        new_pass = Entry(win, show="*")
        new_pass.pack(pady=5)

        Button(win,
               text="Reset",
               bg="#2563eb",
               fg="white",
               command=lambda: messagebox.showinfo("Success", "Password Reset")
               ).pack(pady=15)

   
    def set_password(self):
        username = self.fp_username.get()
        new_password = self.fp_new_password.get()

        if username == "" or new_password == "":
            messagebox.showerror(
                "Error",
                "All fields are required"
            )
            return

        conn = connect_db()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                UPDATE users
                SET password = %s
                WHERE username = %s
                """,
                (new_password, username)
            )

            conn.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo(
                    "Success",
                    "Password Reset Successfully"
                )

                self.fp_username.delete(0, END)
                self.fp_new_password.delete(0, END)

            else:
                messagebox.showerror(
                    "Error",
                    "Username not found"
                )

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                f"{e}"
            )

        finally:
            conn.close()

    def reset_password(self):
        username = self.fp_username.get()
        new_password = self.fp_new_password.get()

        if username == "" or new_password == "":
            messagebox.showerror(
                "Error",
                "All fields are required"
            )
            return

        conn = connect_db()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                UPDATE users
                SET password = %s
                WHERE username = %s
                """,
                (new_password, username)
            )

            conn.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo(
                    "Success",
                    "Password Reset Successfully"
                )

                self.fp_username.delete(0, END)
                self.fp_new_password.delete(0, END)

            else:
                messagebox.showerror(
                    "Error",
                    "Username not found"
                )

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                f"{e}"
            )

        finally:
            conn.close()

        

        # ---------------- SIGN UP WINDOW ----------------
    def signup_window(self):
       
        win = Toplevel(self.root)   # ✅ correct parent
        self.set_background(win, "dash11.png")
        win.title("Sign Up")
        win.geometry("400x350")
        win.configure(bg="#0b1120")

        win.grab_set()  # ✅ makes it focus (prevents background interaction)

        # ===== CARD FRAME =====
        card = Frame(win, bg="#111827")
        card.place(relx=0.5, rely=0.5, anchor="center", width=320, height=280)

        Label(card,
              text="Register",
              font=("Segoe UI", 14, "bold"),
              bg="#111827",
              fg="white").pack(pady=15)

        # Username
        Label(card, text="Username", bg="#111827", fg="#9ca3af").pack(anchor="w", padx=20)
        self.signup_username = Entry(card, bg="#1f2937", fg="white", bd=0)
        self.signup_username.pack(fill="x", padx=20, pady=5, ipady=5)

        # Password
        Label(card, text="Password", bg="#111827", fg="#9ca3af").pack(anchor="w", padx=20)
        self.signup_password = Entry(card, show="*", bg="#1f2937", fg="white", bd=0)
        self.signup_password.pack(fill="x", padx=20, pady=5, ipady=5)

        # Confirm Password
        Label(card, text="Confirm Password", bg="#111827", fg="#9ca3af").pack(anchor="w", padx=20)
        self.signup_confirm = Entry(card, show="*", bg="#1f2937", fg="white", bd=0)
        self.signup_confirm.pack(fill="x", padx=20, pady=5, ipady=5)

        # Register Button
        Button(card,
               text="Register",
               bg="#16a34a",
               fg="white",
               bd=0,
               command=self.register_user).pack(pady=15)

# ---------------- REGISTER USER ----------------
    def register_user(self):
        username = self.signup_username.get()
        password = self.signup_password.get()
        confirm_password = self.signup_confirm.get()

        if username == "" or password == "" or confirm_password == "":
            messagebox.showerror(
                "Error",
                "All fields are required"
            )
            return

        if password != confirm_password:
            messagebox.showerror(
                "Error",
                "Passwords do not match"
            )
            return

        conn = connect_db()
        cursor = conn.cursor()

        try:
            # Check if username already exists
            cursor.execute(
                "SELECT * FROM users WHERE username = %s",
                (username,)
            )

            existing_user = cursor.fetchone()

            if existing_user:
                messagebox.showerror(
                    "Error",
                    "Username already exists"
                )
                return

            # Insert new user
            cursor.execute(
                """
                INSERT INTO users (username, password)
                VALUES (%s, %s)
                """,
                (username, password)
            )

            conn.commit()

            messagebox.showinfo(
                "Success",
                "Registration Successful"
            )

            self.signup_username.delete(0, END)
            self.signup_password.delete(0, END)
            self.signup_confirm.delete(0, END)

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                f"{e}"
            )

        finally:
            conn.close()

        # Hide Image
        self.hide_image = Image.open("SHOW.jpeg")
        self.hide_image = self.hide_image.resize((25,25))
        self.hide_photo = ImageTk.PhotoImage(self.hide_image)

    # 👁 SHOW PASSWORD
    def show(self):
        self.hide_button = Button(
            self.lgn_frame,
            image=self.hide_photo,
            bg="white",
            activebackground="white",
            cursor="hand2",
            bd=0,
            command=self.hide
        )
        self.hide_button.place(x=860, y=420)

        self.password_entry.config(show="")

    # 🙈 HIDE PASSWORD
    def hide(self):
        self.show_button = Button(
            self.lgn_frame,
            image=self.show_photo,
            bg="white",
            activebackground="white",
            cursor="hand2",
            bd=0,
            command=self.show
        )
        self.show_button.place(x=860, y=420)

        self.password_entry.config(show="*")

            
    def open_dashboard(self):
        # destroy login window UI
        for widget in self.root.winfo_children():
            widget.destroy()

        # call dashboard
        self.dashboard()


#================ DASHBOARD =================

    
    def dashboard(self):

        dash = self.root
        dash.title("Inventory Management System")
        dash.geometry("1200x700")
        dash.configure(bg="#0f172a")

        from PIL import Image, ImageTk

        bg = Image.open("dash.jpeg")
        bg = bg.resize((1200, 700))

        self.bg_photo = ImageTk.PhotoImage(bg)

        bg_label = Label(dash, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        from tkinter.ttk import Style
        style = Style()
        style.theme_use("default")

        style.configure("Treeview",
                        background="#111827",
                        foreground="white",
                        rowheight=28,
                        fieldbackground="#111827")

        style.configure("Treeview.Heading",
                        background="#1f2937",
                        foreground="white",
                        font=("Segoe UI", 10, "bold"))

        style.map("Treeview",
                  background=[("selected", "#2563eb")])


        # ================= DATABASE DATA FIRST =================
        data = self.get_dashboard_data()

        total_products = data.get("total_products", 0)
        low_stock = data.get("low_stock", 0)
        today_sales = data.get("today_sales", 0)
        monthly_sales = data.get("monthly_sales", 0)

        # ================= MAIN LAYOUT =================
        container = Frame(dash, bg="#0f172a")
        container.pack(fill=BOTH, expand=True)

        # ================= SIDEBAR =================
        sidebar = Frame(container, bg="#111827", width=220)
        sidebar.pack(side=LEFT, fill=Y)

        Label(
            sidebar,
            text="IMS",
            font=("Segoe UI", 18, "bold"),
            bg="#111827",
            fg="white"
        ).pack(pady=20)

        def menu_btn(text, cmd):
            Button(
                sidebar,
                text=text,
                font=("Segoe UI", 11),
                bg="#111827",
                fg="white",
                bd=0,
                width=20,
                anchor="w",
                command=cmd
            ).pack(pady=5, padx=10)

        menu_btn("Dashboard", lambda: None)
        menu_btn("Add Product", self.add_product_window)
        menu_btn("View Products", self.view_products)
        menu_btn("Sales", self.sales_window)
        menu_btn("Update Product", self.update_product_window)
        menu_btn("Delete Product", self.delete_product_window)
        menu_btn("Logout", dash.destroy)

        # ================= MAIN CONTENT =================
        main = Frame(container, bg="#0f172a")
        main.pack(side=RIGHT, fill=BOTH, expand=True, padx=20, pady=20)

        Label(main, text="Dashboard",
              font=("Segoe UI", 20, "bold"),
              bg="#0f172a", fg="white").pack(anchor="w")

        Label(main, text="Welcome back, Admin 👋",
              font=("Segoe UI", 11),
              bg="#0f172a", fg="#cbd5e1").pack(anchor="w", pady=(0, 20))

        # ================= CARDS =================
        cards_frame = Frame(main, bg="#0f172a")
        cards_frame.pack(fill=X)

        def create_card(parent, title, value, color):
            card = Frame(parent, bg=color, width=200, height=100)
            card.pack(side=LEFT, padx=10)
            card.pack_propagate(False)

            Label(card, text=title,
                  bg=color, fg="white",
                  font=("Segoe UI", 10)).pack(pady=10)

            Label(card, text=str(value),
                  bg=color, fg="white",
                  font=("Segoe UI", 16, "bold")).pack()

        create_card(cards_frame, "Total Products", total_products, "#1e40af")
        create_card(cards_frame, "Sales Today", f"₹ {today_sales}", "#065f46")
        create_card(cards_frame, "Monthly Sales", f"₹ {monthly_sales}", "#92400e")
        create_card(cards_frame, "Low Stock", low_stock, "#7f1d1d")

        # ================= QUICK ACTIONS =================
        Label(main, text="Quick Actions",
              font=("Segoe UI", 14, "bold"),
              bg="#0f172a", fg="white").pack(anchor="w", pady=20)

        actions = Frame(main, bg="#0f172a")
        actions.pack()

        def action_btn(text, cmd, color):
            Button(
                actions,
                text=text,
                width=18,
                height=2,
                bg=color,
                fg="white",
                bd=0,
                command=cmd
            ).pack(side=LEFT, padx=10)

        action_btn("Add Product", self.add_product_window, "#16a34a")
        action_btn("View Products", self.view_products, "#2563eb")
        action_btn("Sales", self.sales_window, "#f59e0b")
        action_btn("Delete", self.delete_product_window, "#dc2626")

        # ================= BOTTOM SECTION =================
        bottom = Frame(main, bg="#0b1120")
        bottom.pack(fill=BOTH, expand=True, pady=20)

        # -------- RECENT SALES (BIG CARD) --------
        sales_card = Frame(bottom, bg="#111827", bd=0,width=500)
        sales_card.pack(side=LEFT, fill=BOTH, expand=True, padx=10)

        Label(sales_card,
              text="Recent Sales",
              bg="#111827",
              fg="white",
              font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=15, pady=10)

        sales_table = Treeview(
            sales_card,
            columns=("ID", "PID", "QTY", "TOTAL"),
            show="headings"
        )

        sales_table.heading("ID", text="Sale ID")
        sales_table.heading("PID", text="Product ID")
        sales_table.heading("QTY", text="Qty")
        sales_table.heading("TOTAL", text="Total ₹")

        sales_table.column("ID", width=70, anchor="center")
        sales_table.column("PID", width=90, anchor="center")
        sales_table.column("QTY", width=60, anchor="center")
        sales_table.column("TOTAL", width=100, anchor="center")

        sales_table.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Load data
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT sale_id, product_id, quantity_sold, total_amount
        FROM sales ORDER BY sale_id DESC LIMIT 5
        """)

        for row in cursor.fetchall():
            sales_table.insert("", END, values=row)

        conn.close()


        # -------- LOW STOCK (SMALL CARD) --------
        stock_card = Frame(bottom, bg="#111827", width=300)
        stock_card.pack(side=RIGHT, fill=Y, padx=10)
        stock_card.pack_propagate(False)

        Label(stock_card,
              text="Low Stock Alert",
              bg="#111827",
              fg="#ef4444",
              font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=15, pady=10)

        stock_table = Treeview(
            stock_card,
            columns=("ID", "NAME", "QTY"),
            show="headings",
            height=6
        )

        stock_table.heading("ID", text="ID")
        stock_table.heading("NAME", text="Product Name")
        stock_table.heading("QTY", text="Qty")

        stock_table.column("ID", width=30, anchor="center")
        stock_table.column("NAME", width=100, anchor="center")
        stock_table.column("QTY", width=50, anchor="center")


        stock_table.pack(fill=BOTH, expand=True, padx=15, pady=10)

        # Load low stock
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT product_id, product_name, quantity
        FROM products WHERE quantity < 10
        """)

        rows = cursor.fetchall()

        if rows:
            for row in rows:
                stock_table.insert("", END, values=row)
        else:
            stock_table.insert("", END, values=("—", "No low stock", "✔"))

        conn.close()
    #=================================Card Database=============================================
    def get_dashboard_data(self):
        conn = connect_db()
        cursor = conn.cursor()

        data = {}

        try:
            cursor.execute("SELECT COUNT(*) FROM products")
            data["total_products"] = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM products WHERE quantity < 10")
            data["low_stock"] = cursor.fetchone()[0]

            cursor.execute("""
                SELECT IFNULL(SUM(total_amount),0)
                FROM sales
                WHERE sale_date = CURDATE()
            """)
            data["today_sales"] = cursor.fetchone()[0]

            cursor.execute("""
                SELECT IFNULL(SUM(total_amount),0)
                FROM sales
                WHERE MONTH(sale_date) = MONTH(CURDATE())
            """)
            data["monthly_sales"] = cursor.fetchone()[0]

        except Exception as e:
            messagebox.showerror("Database Error", str(e))

        finally:
            conn.close()

        return data
    #-------------- ADD PRODUCT ----------------
    def add_product_window(self):
        win = Toplevel(self.root)
        win.title("Add Product")
        win.geometry("500x450")
        win.configure(bg="#0b1120")

        # ===== MAIN CARD =====
        card = Frame(win, bg="#111827", bd=0)
        card.place(relx=0.5, rely=0.5, anchor="center", width=400, height=380)

        # ===== TITLE =====
        Label(card,
              text="Add New Product",
              font=("Segoe UI", 16, "bold"),
              bg="#111827",
              fg="white").pack(pady=20)

        # ===== NAME =====
        Label(card, text="Product Name",
              bg="#111827", fg="#9ca3af",
              font=("Segoe UI", 10)).pack(anchor="w", padx=30)

        self.name = Entry(card,
                          bg="#1f2937",
                          fg="white",
                          bd=0,
                          font=("Segoe UI", 11))
        self.name.pack(fill="x", padx=30, pady=5, ipady=6)

        # ===== PRICE =====
        Label(card, text="Price",
              bg="#111827", fg="#9ca3af",
              font=("Segoe UI", 10)).pack(anchor="w", padx=30, pady=(10,0))

        self.price = Entry(card,
                           bg="#1f2937",
                           fg="white",
                           bd=0,
                           font=("Segoe UI", 11))
        self.price.pack(fill="x", padx=30, pady=5, ipady=6)

        # ===== QUANTITY =====
        Label(card, text="Quantity",
              bg="#111827", fg="#9ca3af",
              font=("Segoe UI", 10)).pack(anchor="w", padx=30, pady=(10,0))

        self.qty = Entry(card,
                         bg="#1f2937",
                         fg="white",
                         bd=0,
                         font=("Segoe UI", 11))
        self.qty.pack(fill="x", padx=30, pady=5, ipady=6)

        # ===== BUTTON FRAME =====
        btn_frame = Frame(card, bg="#111827")
        btn_frame.pack(pady=20)

        # SAVE BUTTON
        Button(btn_frame,
               text="💾 Save",
               bg="#16a34a",
               fg="white",
               font=("Segoe UI", 10, "bold"),
               bd=0,
               width=12,
               cursor="hand2",
               command=self.save).pack(side=LEFT, padx=10)

        # CLEAR BUTTON
        Button(btn_frame,
               text="Clear",
               bg="#374151",
               fg="white",
               font=("Segoe UI", 10),
               bd=0,
               width=12,
               cursor="hand2",
               #command=self.clear_add_form).pack(side=LEFT, padx=10
               )
    def save(self):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (product_name, price, quantity) VALUES (%s,%s,%s)",
                           (self.name.get(), self.price.get(), self.qty.get()))
        conn.commit()
        messagebox.showinfo("Success", "Product Added")


        
# ---------------- VIEW PRODUCTS ----------------
    def view_products(self):
        win = Toplevel(self.root)
        win.title("View Products")
        win.geometry("800x500")
        win.configure(bg="#0b1120")

        # ===== TITLE =====
        Label(win,
              text="Products List",
              font=("Segoe UI", 16, "bold"),
              bg="#0b1120",
              fg="white").pack(pady=10)

        # ===== FRAME (CARD STYLE) =====
        card = Frame(win, bg="#111827")
        card.pack(fill=BOTH, expand=True, padx=20, pady=10)

        # ===== TREEVIEW STYLE =====
        from tkinter.ttk import Style
        style = Style()
        style.theme_use("default")

        style.configure("Treeview",
                        background="#111827",
                        foreground="white",
                        rowheight=28,
                        fieldbackground="#111827")

        style.configure("Treeview.Heading",
                        background="#1f2937",
                        foreground="white",
                        font=("Segoe UI", 10, "bold"))

        style.map("Treeview",
                  background=[("selected", "#2563eb")])

        # ===== TABLE =====
        self.product_table = Treeview(
            card,
            columns=("ID", "Name", "Price", "Qty"),
            show="headings"
        )

        self.product_table.heading("ID", text="ID")
        self.product_table.heading("Name", text="Product Name")
        self.product_table.heading("Price", text="Price")
        self.product_table.heading("Qty", text="Quantity")

        # ===== COLUMN WIDTH =====
        self.product_table.column("ID", width=60, anchor="center")
        self.product_table.column("Name", width=200)
        self.product_table.column("Price", width=100, anchor="center")
        self.product_table.column("Qty", width=80, anchor="center")

        self.product_table.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # ===== SCROLLBAR =====
        scrollbar = Scrollbar(card, orient=VERTICAL, command=self.product_table.yview)
        self.product_table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)

        # ===== LOAD DATA =====
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("SELECT product_id, product_name, price, quantity FROM products")

        rows = cursor.fetchall()

        for row in rows:
            # Highlight low stock
            if row[3] < 10:
                self.product_table.insert("", END, values=row, tags=("low",))
            else:
                self.product_table.insert("", END, values=row)

        conn.close()

        # ===== LOW STOCK STYLE =====
        self.product_table.tag_configure("low", foreground="red")

        # ===== REFRESH BUTTON =====
        Button(win,
               text="🔄 Refresh",
               bg="#2563eb",
               fg="white",
               bd=0,
               font=("Segoe UI", 10, "bold"),
               command=self.refresh_products).pack(pady=10)
    def refresh_products(self):
        for row in self.product_table.get_children():
            self.product_table.delete(row)

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("SELECT product_id, product_name, price, quantity FROM products")

        for row in cursor.fetchall():
            if row[3] < 10:
                self.product_table.insert("", END, values=row, tags=("low",))
            else:
                self.product_table.insert("", END, values=row)

        conn.close()
# ---------------- SALES ----------------
    def sales_window(self):
        win = Toplevel(self.root)
        win.title("Sales")
        win.geometry("900x550")
        win.configure(bg="#0b1120")

        # ===== TITLE =====
        Label(win,
              text="Sales Management",
              font=("Segoe UI", 16, "bold"),
              bg="#0b1120",
              fg="white").pack(pady=10)

        # ===== MAIN FRAME =====
        main = Frame(win, bg="#0b1120")
        main.pack(fill=BOTH, expand=True, padx=20)

        # ================= LEFT (FORM) =================
        form_card = Frame(main, bg="#111827", width=300)
        form_card.pack(side=LEFT, fill=Y, padx=10)
        form_card.pack_propagate(False)

        Label(form_card, text="Generate Bill",
              bg="#111827", fg="white",
              font=("Segoe UI", 12, "bold")).pack(pady=15)

        # Product ID
        Label(form_card, text="Product ID",
              bg="#111827", fg="#9ca3af").pack(anchor="w", padx=20)
        self.pid = Entry(form_card, bg="#1f2937", fg="white", bd=0)
        self.pid.pack(fill="x", padx=20, pady=5, ipady=6)

        # Quantity
        Label(form_card, text="Quantity",
              bg="#111827", fg="#9ca3af").pack(anchor="w", padx=20, pady=(10,0))
        self.qty = Entry(form_card, bg="#1f2937", fg="white", bd=0)
        self.qty.pack(fill="x", padx=20, pady=5, ipady=6)

        # Button
        Button(form_card,
               text="💰 Generate Bill",
               bg="#16a34a",
               fg="white",
               bd=0,
               font=("Segoe UI", 10, "bold"),
               command=self.sell).pack(pady=20)

        # ================= RIGHT (TABLE) =================
        table_card = Frame(main, bg="#111827")
        table_card.pack(side=RIGHT, fill=BOTH, expand=True, padx=10)

        Label(table_card,
              text="Sales Report",
              bg="#111827",
              fg="white",
              font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=10, pady=10)

        # ===== STYLE =====
        from tkinter.ttk import Style
        style = Style()
        style.theme_use("default")

        style.configure("Treeview",
                        background="#111827",
                        foreground="white",
                        rowheight=28,
                        fieldbackground="#111827")

        style.configure("Treeview.Heading",
                        background="#1f2937",
                        foreground="white")

        # ===== TABLE =====
        self.sales_tree = Treeview(
            table_card,
            columns=("ID", "PID", "QTY", "TOTAL"),
            show="headings"
        )

        self.sales_tree.heading("ID", text="Sale ID")
        self.sales_tree.heading("PID", text="Product ID")
        self.sales_tree.heading("QTY", text="Qty")
        self.sales_tree.heading("TOTAL", text="Total ₹")

        self.sales_tree.column("ID", width=80, anchor="center")
        self.sales_tree.column("PID", width=100, anchor="center")
        self.sales_tree.column("QTY", width=80, anchor="center")
        self.sales_tree.column("TOTAL", width=120, anchor="center")

        self.sales_tree.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # ===== SCROLLBAR =====
        scrollbar = Scrollbar(table_card, orient=VERTICAL, command=self.sales_tree.yview)
        self.sales_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)

        # ================= BUTTONS =================
        btn_frame = Frame(win, bg="#0b1120")
        btn_frame.pack(pady=10)

        Button(btn_frame,
               text="📅 Daily Report",
               bg="#2563eb",
               fg="white",
               bd=0,
               command=self.daily_sales_report_window).pack(side=LEFT, padx=10)

        Button(btn_frame,
               text="📆 Monthly Report",
               bg="#f59e0b",
               fg="white",
               bd=0,
               command=self.monthly_sales_report_window).pack(side=LEFT, padx=10)

        Button(btn_frame,
               text="🔄 Refresh",
               bg="#6b7280",
               fg="white",
               bd=0,
               command=self.load_sales_data).pack(side=LEFT, padx=10)

        # Load initial data
        self.load_sales_data()


    def load_sales_data(self):
        for row in self.sales_tree.get_children():
            self.sales_tree.delete(row)

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT sale_id, product_id, quantity_sold, total_amount
            FROM sales
            ORDER BY sale_id DESC
        """)

        for row in cursor.fetchall():
            self.sales_tree.insert("", END, values=row)

        conn.close()
        #============================Generate BIll=====================================

    def print_bill(self, product_id, qty_sold, total):
        bill = Toplevel(self.root)
        bill.title("Invoice")
        bill.geometry("400x450")
        bill.configure(bg="#0b1120")

        # ===== MAIN CARD =====
        card = Frame(bill, bg="#111827")
        card.place(relx=0.5, rely=0.5, anchor="center", width=350, height=400)

        # ===== TITLE =====
        Label(card,
              text="🧾 INVOICE",
              font=("Segoe UI", 16, "bold"),
              bg="#111827",
              fg="white").pack(pady=10)

        Label(card,
              text="Inventory System",
              font=("Segoe UI", 10),
              bg="#111827",
              fg="#9ca3af").pack()

        # ===== LINE =====
        Frame(card, bg="#374151", height=2).pack(fill="x", padx=20, pady=10)

        # ===== BILL DETAILS =====
        Label(card,
              text=f"Product ID : {product_id}",
              bg="#111827", fg="white",
              font=("Segoe UI", 10)).pack(anchor="w", padx=20, pady=5)

        Label(card,
              text=f"Quantity   : {qty_sold}",
              bg="#111827", fg="white",
              font=("Segoe UI", 10)).pack(anchor="w", padx=20, pady=5)

        Label(card,
              text=f"Total ₹    : {total}",
              bg="#111827", fg="#22c55e",
              font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=20, pady=10)

        # ===== LINE =====
        Frame(card, bg="#374151", height=2).pack(fill="x", padx=20, pady=10)

        # ===== FOOTER =====
        Label(card,
              text="Thank You! Visit Again 😊",
              bg="#111827",
              fg="#9ca3af",
              font=("Segoe UI", 10)).pack(pady=10)

        # ===== BUTTONS =====
        btn_frame = Frame(card, bg="#111827")
        btn_frame.pack(pady=10)

        Button(btn_frame,
               text="Close",
               bg="#ef4444",
               fg="white",
               bd=0,
               width=10,
               command=bill.destroy).pack(side=LEFT, padx=10)

        Button(btn_frame,
               text="Print",
               bg="#2563eb",
               fg="white",
               bd=0,
               width=10,
               command=lambda: self.print_to_console(product_id, qty_sold, total)
               ).pack(side=LEFT, padx=10)
    def print_to_console(self, product_id, qty_sold, total):
        print("----- BILL -----")
        print("Product ID:", product_id)
        print("Quantity:", qty_sold)
        print("Total:", total)
        print("----------------")
           
        # ---------------- DAILY SALES REPORT ----------------
    def daily_sales_report_window(self):
        win = Toplevel(self.root)
        win.title("Daily Sales Report")
        win.geometry("800x500")
        win.configure(bg="#0b1120")

        # ===== TITLE =====
        Label(win,
              text="📅 Daily Sales Report",
              font=("Segoe UI", 16, "bold"),
              bg="#0b1120",
              fg="white").pack(pady=10)

        # ===== CARD =====
        card = Frame(win, bg="#111827")
        card.pack(fill=BOTH, expand=True, padx=20, pady=10)

        # ===== TABLE =====
        self.daily_tree = Treeview(
            card,
            columns=("SaleID", "ProductID", "Qty", "Total"),
            show="headings"
        )

        self.daily_tree.heading("SaleID", text="Sale ID")
        self.daily_tree.heading("ProductID", text="Product ID")
        self.daily_tree.heading("Qty", text="Quantity")
        self.daily_tree.heading("Total", text="Total ₹")

        self.daily_tree.column("SaleID", width=80, anchor="center")
        self.daily_tree.column("ProductID", width=100, anchor="center")
        self.daily_tree.column("Qty", width=80, anchor="center")
        self.daily_tree.column("Total", width=120, anchor="center")

        self.daily_tree.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # ===== SCROLLBAR =====
        scrollbar = Scrollbar(card, orient=VERTICAL, command=self.daily_tree.yview)
        self.daily_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)

        # ===== LOAD DATA =====
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT sale_id, product_id, quantity_sold, total_amount
            FROM sales
            WHERE sale_date = CURDATE()
            ORDER BY sale_id DESC
        """)

        total_sum = 0

        for row in cursor.fetchall():
            self.daily_tree.insert("", END, values=row)
            total_sum += row[3]

        conn.close()

        # ===== TOTAL DISPLAY =====
        Label(win,
              text=f"Total Sales Today: ₹ {total_sum}",
              font=("Segoe UI", 12, "bold"),
              bg="#0b1120",
              fg="#22c55e").pack(pady=10)

# ---------------- MONTHLY SALES REPORT ----------------
    def monthly_sales_report_window(self):
        win = Toplevel(self.root)
        win.title("Monthly Sales Report")
        win.geometry("850x520")
        win.configure(bg="#0b1120")

        # ===== TITLE =====
        Label(win,
              text="📆 Monthly Sales Report",
              font=("Segoe UI", 16, "bold"),
              bg="#0b1120",
              fg="white").pack(pady=10)

        # ===== CARD =====
        card = Frame(win, bg="#111827")
        card.pack(fill=BOTH, expand=True, padx=20, pady=10)

        # ===== TABLE =====
        self.monthly_tree = Treeview(
            card,
            columns=("SaleID", "ProductID", "Qty", "Total", "Date"),
            show="headings"
        )

        self.monthly_tree.heading("SaleID", text="Sale ID")
        self.monthly_tree.heading("ProductID", text="Product ID")
        self.monthly_tree.heading("Qty", text="Quantity")
        self.monthly_tree.heading("Total", text="Total ₹")
        self.monthly_tree.heading("Date", text="Date")

        self.monthly_tree.column("SaleID", width=80, anchor="center")
        self.monthly_tree.column("ProductID", width=100, anchor="center")
        self.monthly_tree.column("Qty", width=80, anchor="center")
        self.monthly_tree.column("Total", width=120, anchor="center")
        self.monthly_tree.column("Date", width=120, anchor="center")

        self.monthly_tree.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # ===== SCROLLBAR =====
        scrollbar = Scrollbar(card, orient=VERTICAL, command=self.monthly_tree.yview)
        self.monthly_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)

        # ===== LOAD DATA =====
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT sale_id, product_id, quantity_sold, total_amount, sale_date
            FROM sales
            WHERE MONTH(sale_date) = MONTH(CURDATE())
              AND YEAR(sale_date) = YEAR(CURDATE())
            ORDER BY sale_id DESC
        """)

        total_sum = 0

        for row in cursor.fetchall():
            self.monthly_tree.insert("", END, values=row)
            total_sum += row[3]

        conn.close()

        # ===== TOTAL DISPLAY =====
        Label(win,
              text=f"Total Sales This Month: ₹ {total_sum}",
              font=("Segoe UI", 12, "bold"),
              bg="#0b1120",
              fg="#22c55e").pack(pady=10)

        # ===== REFRESH BUTTON =====
        Button(win,
               text="🔄 Refresh",
               bg="#2563eb",
               fg="white",
               bd=0,
               command=self.monthly_sales_report_window).pack(pady=5)
    def sell(self):
        conn = connect_db()
        cursor = conn.cursor()

        try:
            # Get product stock and price using product_id
            cursor.execute(
                "SELECT quantity, price FROM products WHERE product_id = %s",
                (self.pid.get(),)
            )

            result = cursor.fetchone()

            if result:
                stock, price = result
                qty_sold = int(self.qty.get())

                # Check stock availability
                if qty_sold <= stock:
                    new_stock = stock - qty_sold
                    total = qty_sold * price

                    # Update remaining stock
                    cursor.execute(
                        "UPDATE products SET quantity = %s WHERE product_id = %s",
                        (new_stock, self.pid.get())
                    )

                    # Insert sales record
                    cursor.execute(
                        """
                        INSERT INTO sales
                        (product_id, quantity_sold, total_amount, sale_date)
                        VALUES (%s, %s, %s, CURDATE())
                        """,
                        (self.pid.get(), qty_sold, total)
                    )

                    conn.commit()

                    self.print_bill(
                    self.pid.get(),
                    qty_sold,
                    total
                )
                    # Clear fields after success
                    self.pid.delete(0, END)
                    self.qty.delete(0, END)

                else:
                    messagebox.showerror(
                        "Error",
                        "Not enough stock available"
                    )

            else:
                messagebox.showerror(
                    "Error",
                    "Product not found"
                )

        except ValueError:
            messagebox.showerror(
                "Error",
                "Please enter valid numeric values"
            )

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                f"{e}"
            )

        finally:
            conn.close()

    #==============================update Product=================
    def update_product_window(self):
        win = Toplevel(self.root)
        win.title("Update Product")
        win.geometry("500x800")
        win.configure(bg="#0b1120")

        # ===== MAIN CARD =====
        card = Frame(win, bg="#111827")
        card.place(relx=0.5, rely=0.5, anchor="center", width=420, height=600)

        # ===== TITLE =====
        Label(card,
              text="Update Product",
              font=("Segoe UI", 16, "bold"),
              bg="#111827",
              fg="white").pack(pady=20)

        # ===== PRODUCT ID =====
        Label(card, text="Product ID",
              bg="#111827", fg="#9ca3af",
              font=("Segoe UI", 10)).pack(anchor="w", padx=30)

        self.update_pid = Entry(card,
                                bg="#1f2937",
                                fg="white",
                                bd=0,
                                font=("Segoe UI", 11))
        self.update_pid.pack(fill="x", padx=30, pady=5, ipady=6)

        # ===== PRODUCT NAME =====
        Label(card, text="Product Name",
              bg="#111827", fg="#9ca3af",
              font=("Segoe UI", 10)).pack(anchor="w", padx=30, pady=(10,0))

        self.update_name = Entry(card,
                                 bg="#1f2937",
                                 fg="white",
                                 bd=0,
                                 font=("Segoe UI", 11))
        self.update_name.pack(fill="x", padx=30, pady=5, ipady=6)

        # ===== PRICE =====
        Label(card, text="Price",
              bg="#111827", fg="#9ca3af",
              font=("Segoe UI", 10)).pack(anchor="w", padx=30, pady=(10,0))

        self.update_price = Entry(card,
                                  bg="#1f2937",
                                  fg="white",
                                  bd=0,
                                  font=("Segoe UI", 11))
        self.update_price.pack(fill="x", padx=30, pady=5, ipady=6)

        # ===== QUANTITY =====
        Label(card, text="Quantity",
              bg="#111827", fg="#9ca3af",
              font=("Segoe UI", 10)).pack(anchor="w", padx=30, pady=(10,0))

        self.update_qty = Entry(card,
                                bg="#1f2937",
                                fg="white",
                                bd=0,
                                font=("Segoe UI", 11))
        self.update_qty.pack(fill="x", padx=30, pady=5, ipady=6)

        # ===== BUTTONS =====
        btn_frame = Frame(card, bg="#111827")
        btn_frame.pack(pady=25)

        # UPDATE BUTTON
        update_btn = Button(btn_frame,
                            text="🔄 Update",
                            bg="#2563eb",
                            fg="white",
                            font=("Segoe UI", 10, "bold"),
                            bd=0,
                            width=12,
                            cursor="hand2",
                            command=self.update_product)
        update_btn.pack(side=LEFT, padx=10)

        # CLEAR BUTTON
        clear_btn = Button(btn_frame,
                           text="Clear",
                           bg="#374151",
                           fg="white",
                           font=("Segoe UI", 10),
                           bd=0,
                           width=12,
                           cursor="hand2",
                           command=self.clear_update_form)
        clear_btn.pack(side=LEFT, padx=10)

    def update_product(self):
                conn = connect_db()
                cursor = conn.cursor()

                try:
                    cursor.execute(
                        """
                        UPDATE products
                        SET product_name = %s,
                            price = %s,
                            quantity = %s
                        WHERE product_id = %s
                        """,
                        (
                            self.update_name.get(),
                            self.update_price.get(),
                            self.update_qty.get(),
                            self.update_pid.get()
                        )
                    )

                    conn.commit()

                    if cursor.rowcount > 0:
                        messagebox.showinfo(
                            "Success",
                            "Product Updated Successfully"
                        )

                        self.update_pid.delete(0, END)
                        self.update_name.delete(0, END)
                        self.update_price.delete(0, END)
                        self.update_qty.delete(0, END)

                    else:
                        messagebox.showerror(
                            "Error",
                            "Product ID not found"
                        )

                except Exception as e:
                    messagebox.showerror(
                        "Database Error",
                        f"{e}"
                    )

                finally:
                    conn.close()
    def clear_update_form(self):
        self.update_pid.delete(0, END)
        self.update_name.delete(0, END)
        self.update_price.delete(0, END)
        self.update_qty.delete(0, END)

        #=====================Delete Product=========================================================================
    def delete_product_window(self):
        win = Toplevel(self.root)
        win.title("Delete Product")
        win.geometry("750x450")
        win.configure(bg="#0b1120")

        # ===== TITLE =====
        Label(win,
              text="Delete Product",
              font=("Segoe UI", 16, "bold"),
              bg="#0b1120",
              fg="white").pack(pady=10)

        # ===== CARD =====
        card = Frame(win, bg="#111827")
        card.pack(fill=BOTH, expand=True, padx=20, pady=10)

        # ===== TABLE =====
        self.delete_table = Treeview(
            card,
            columns=("ID", "Name", "Price", "Qty"),
            show="headings"
        )

        self.delete_table.heading("ID", text="ID")
        self.delete_table.heading("Name", text="Product Name")
        self.delete_table.heading("Price", text="Price")
        self.delete_table.heading("Qty", text="Quantity")

        self.delete_table.column("ID", width=60, anchor="center")
        self.delete_table.column("Name", width=200)
        self.delete_table.column("Price", width=100, anchor="center")
        self.delete_table.column("Qty", width=80, anchor="center")

        self.delete_table.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # ===== SCROLLBAR =====
        scrollbar = Scrollbar(card, orient=VERTICAL, command=self.delete_table.yview)
        self.delete_table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)

        # ===== LOAD DATA =====
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT product_id, product_name, price, quantity FROM products")

        for row in cursor.fetchall():
            self.delete_table.insert("", END, values=row)

        conn.close()

        # ===== BUTTON =====
        Button(win,
               text="🗑 Delete Selected",
               bg="#dc2626",
               fg="white",
               font=("Segoe UI", 10, "bold"),
               bd=0,
               command=self.delete_selected_product).pack(pady=10)
        
    def delete_product(self):
        conn = connect_db()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "DELETE FROM products WHERE product_id = %s",
                (self.delete_pid.get(),)
            )

            conn.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo(
                    "Success",
                    "Product Deleted Successfully"
                )

                self.delete_pid.delete(0, END)

            else:
                messagebox.showerror(
                    "Error",
                    "Product ID not found"
                )

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                f"{e}"
            )

        finally:
            conn.close()

    def delete_selected_product(self):
        selected = self.delete_table.focus()

        if not selected:
            messagebox.showerror("Error", "Please select a product")
            return

        values = self.delete_table.item(selected, "values")
        product_id = values[0]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete Product ID {product_id}?"
        )

        if not confirm:
            return

        conn = connect_db()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "DELETE FROM products WHERE product_id = %s",
                (product_id,)
            )
            conn.commit()

            messagebox.showinfo("Success", "Product Deleted Successfully")

            # Remove from table
            self.delete_table.delete(selected)

        except Exception as e:
            messagebox.showerror("Database Error", f"{e}")

        finally:
            conn.close()

def page():
    window = Tk()
    LoginForm(window)
    window.mainloop()

if __name__ == "__main__":
    page()
