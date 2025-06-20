from kivy.app import App
from kivy.uix.button import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout


class MatrixMultiplierApp(App):
    def build(self):
        global root
        root=ScreenManager()

        interface=Interface()

        #Home screen
        global home_screen
        hs=interface.homescreen()
        home_screen=Screen(name='home_screen')
        home_screen.add_widget(hs)
        root.add_widget(home_screen)

        #Matrix input screen
        global input_screen
        iS=interface.matrixInputScreen()
        input_screen=Screen(name='input_screen')
        input_screen.add_widget(iS)
        root.add_widget(input_screen)

        return root

class Interface():
    def __init__(self):
        self.matrix1=Matrix()
        self.matrix2=Matrix()
        self.log=''
        self.error=''
        self.matrix1_inputs = []  # Store TextInput widgets for matrix1
        self.matrix2_inputs = []  # Store TextInput widgets for matrix2
        self.result_matrix = None  # Store result for display
    def homescreen(self):
        home=FloatLayout()
        InputBox1=BoxLayout(orientation='horizontal',size_hint=(.5,.05),pos_hint={'left':1,'top':1})
        l1=Label(text='Enter sizes for matrix A : ')
        m1inp=TextInput(size_hint=(.1,1))
        x=Label(text='X',size_hint=(.045,1))
        n1inp=TextInput(size_hint=(.1,1))
        InputBox1.add_widget(l1)
        InputBox1.add_widget(m1inp)
        InputBox1.add_widget(x)
        InputBox1.add_widget(n1inp)

        InputBox2=BoxLayout(orientation='horizontal',size_hint=(.5,.05),pos_hint={'left':1,'top':.95})
        l2=Label(text='Enter sizes for matrix B : ')
        m2inp=TextInput(size_hint=(.1,1))
        x=Label(text='X',size_hint=(.045,1))
        n2inp=TextInput(size_hint=(.1,1))
        InputBox2.add_widget(l2)
        InputBox2.add_widget(m2inp)
        InputBox2.add_widget(x)
        InputBox2.add_widget(n2inp)
        def pressed(instance):
            print(instance)
            try:
                self.matrix1=Matrix(int(m1inp.text),int(n1inp.text))
            except:
                self.error+='Matrix 1 not created correctly\n'
            try:
                self.matrix2=Matrix(int(m2inp.text),int(n2inp.text))
            except:
                self.error+='Matrix 2 not created correctly \n'
            if int(n1inp.text)!=int(m2inp.text):
                self.error+='The matrices are not compatible for multiplication \n'
            if len(self.error)>0:
                errorscreen=self.errorscreen(self.error)
                screen=Screen(name='error_screen')
                screen.add_widget(errorscreen)
                self.errorwidget=screen
                root.add_widget(screen)
                root.transition = SlideTransition(direction='left', duration=.25)   
                root.current = 'error_screen'
            else:
                root.remove_widget(root.get_screen('input_screen'))
                iS=self.matrixInputScreen()
                input_screen=Screen(name='input_screen')
                input_screen.add_widget(iS)
                root.add_widget(input_screen)
                root.transition=SlideTransition(direction='left', duration=.25)
                root.current='input_screen'
            

            
        submit=Button(text='submit',size_hint=(.5,.05),pos_hint={'left':1,'top':.89},on_press=pressed)
            
        home.add_widget(InputBox1)
        home.add_widget(InputBox2)
        home.add_widget(submit)
            
        return home
    
    def errorscreen(self,error_message):
        e=FloatLayout()
        l=Label(text='An error occurred : '+error_message,font_size=30)
        def back(instance):
            print(instance)
            root.remove_widget(self.errorwidget)
            self.log+=self.error
            self.error=''
            root.transition=SlideTransition(direction='right', duration=.25)
            root.current='home_screen'
        button=Button(text='home',on_press=back,size_hint=(.5,.05),pos_hint={'top':1,'left':1})
        e.add_widget(l)
        e.add_widget(button)
        return e
    
    def matrixInputScreen(self):
        self.values=[]
        self.matrix1_inputs = []
        self.matrix2_inputs = []
        s=FloatLayout()
        head=Label(
            text="[b]Enter the matrix entries below[/b]",
            markup=True,
            font_size='24sp',
            size_hint=(1,.12),
            pos_hint={'center_x':0.5, 'top':1},
            halign='center',
            valign='middle'
        )
        head.bind(size=lambda instance, value: setattr(instance, 'text_size', value))
        s.add_widget(head)

        # Matrix A input (left aligned)
        mat1Box=BoxLayout(
            orientation='horizontal',
            size_hint=(None, None),
            width=60+50*self.matrix1.n,
            height=60+50*self.matrix1.m,
            pos_hint={'x':0, 'top':.9}
        )
        mat1Label=Label(
            text='Matrix A : ',
            size_hint=(None,1),
            width=80,
            halign='left',
            valign='middle'
        )
        mat1Label.bind(size=lambda instance, value: setattr(instance, 'text_size', value))
        mat1Box.add_widget(mat1Label)
        grid1 = GridLayout(
            rows=self.matrix1.m,
            cols=self.matrix1.n,
            size_hint=(None, None),
            width=50*self.matrix1.n,
            height=50*self.matrix1.m,
            spacing=5,
            padding=[0,0,0,0]
        )
        for i in range(self.matrix1.m):
            row_inputs = []
            for j in range(self.matrix1.n):
                inp = TextInput(
                    multiline=False,
                    size_hint=(None, None),
                    width=50,
                    height=50,
                    halign='left'
                )
                row_inputs.append(inp)
                grid1.add_widget(inp)
            self.matrix1_inputs.append(row_inputs)
        mat1Box.add_widget(grid1)
        s.add_widget(mat1Box)

        # Matrix B input (left aligned)
        mat2Box=BoxLayout(
            orientation='horizontal',
            size_hint=(None, None),
            width=60+50*self.matrix2.n,
            height=60+50*self.matrix2.m,
            pos_hint={'x':0, 'top':.48}
        )
        mat2Label=Label(
            text='Matrix B : ',
            size_hint=(None,1),
            width=80,
            halign='left',
            valign='middle'
        )
        mat2Label.bind(size=lambda instance, value: setattr(instance, 'text_size', value))
        mat2Box.add_widget(mat2Label)
        grid2 = GridLayout(
            rows=self.matrix2.m,
            cols=self.matrix2.n,
            size_hint=(None, None),
            width=50*self.matrix2.n,
            height=50*self.matrix2.m,
            spacing=5,
            padding=[0,0,0,0]
        )
        for i in range(self.matrix2.m):
            row_inputs = []
            for j in range(self.matrix2.n):
                inp = TextInput(
                    multiline=False,
                    size_hint=(None, None),
                    width=50,
                    height=50,
                    halign='left'
                )
                row_inputs.append(inp)
                grid2.add_widget(inp)
            self.matrix2_inputs.append(row_inputs)
        mat2Box.add_widget(grid2)
        s.add_widget(mat2Box)

        # Add Multiply button below matrix inputs
        def multiply_pressed(instance):
            try:
                # Get values from input fields
                values1 = self.get_matrix1_values()
                values2 = self.get_matrix2_values()
                # Convert to float and validate
                mat1_vals = [[float(val) for val in row] for row in values1]
                mat2_vals = [[float(val) for val in row] for row in values2]
                self.matrix1.set_values(mat1_vals)
                self.matrix2.set_values(mat2_vals)
                # Multiply
                result = self.matrix1.multiply(self.matrix2)
                self.result_matrix = result
                # Show result screen
                solver_screen = Screen(name='matrix_solver')
                solver_screen.add_widget(self.matrixSolverScreen())
                # Remove old solver screen if exists
                if 'matrix_solver' in [s.name for s in root.screens]:
                    root.remove_widget(root.get_screen('matrix_solver'))
                root.add_widget(solver_screen)
                root.transition = SlideTransition(direction='left', duration=.25)
                root.current = 'matrix_solver'
            except Exception as e:
                # Show error screen if invalid input or multiplication error
                errorscreen = self.errorscreen(f"Invalid input or multiplication error: {e}")
                screen = Screen(name='error_screen')
                screen.add_widget(errorscreen)
                self.errorwidget = screen
                root.add_widget(screen)
                root.transition = SlideTransition(direction='left', duration=.25)
                root.current = 'error_screen'

        multiply_btn = Button(
            text='Multiply',
            size_hint=(.2, .07),
            pos_hint={'x':0, 'y':.02},
            on_press=multiply_pressed
        )
        s.add_widget(multiply_btn)
        # Add home button (bottom left)
        def go_home(instance):
            root.transition=SlideTransition(direction='right', duration=.25)
            root.current='home_screen'
        home_btn = Button(text='Home', size_hint=(.15, .07), pos_hint={'x':.5, 'y':.02}, on_press=go_home)
        s.add_widget(home_btn)
        return s

    def matrixSolverScreen(self):
        # Display the result matrix in a grid, similar to input
        layout = FloatLayout()
        head = Label(
            text="[b]Product of Matrix A and Matrix B[/b]",
            markup=True,
            font_size='24sp',
            size_hint=(1,.12),
            pos_hint={'center_x':0.5, 'top':1},
            halign='center',
            valign='middle'
        )
        head.bind(size=lambda instance, value: setattr(instance, 'text_size', value))
        layout.add_widget(head)

        if not self.result_matrix:
            error_label = Label(
                text="No result to display.",
                size_hint=(1, .2),
                pos_hint={'center_x':0.5, 'center_y':0.5}
            )
            layout.add_widget(error_label)
            return layout

        rows = self.result_matrix.m
        cols = self.result_matrix.n
        grid = GridLayout(
            rows=rows,
            cols=cols,
            size_hint=(None, None),
            width=50*cols,
            height=50*rows,
            spacing=5,
            pos_hint={'x':0, 'top':.8}
        )
        for i in range(rows):
            for j in range(cols):
                val = str(self.result_matrix.values[i][j])
                grid.add_widget(Label(
                    text=val,
                    size_hint=(None, None),
                    width=50,
                    height=50,
                    halign='center',
                    valign='middle'
                ))
        layout.add_widget(grid)

        # Add a back button
        def back_pressed(instance):
            root.transition = SlideTransition(direction='right', duration=.25)
            root.current = 'input_screen'
        back_btn = Button(
            text='Back',
            size_hint=(.2, .07),
            pos_hint={'x':0, 'y':.09},
            on_press=back_pressed
        )
        # Add home button (bottom left)
        def go_home(instance):
            root.transition=SlideTransition(direction='right', duration=.25)
            root.current='home_screen'
        home_btn = Button(text='Home', size_hint=(.15, .07), pos_hint={'x':0, 'y':0}, on_press=go_home)
        layout.add_widget(back_btn)
        layout.add_widget(home_btn)
        return layout

    def get_matrix1_values(self):
        # Returns a 2D list of the current values in the matrix1 input fields
        values = []
        for row in self.matrix1_inputs:
            values.append([inp.text for inp in row])
        return values

    def get_matrix2_values(self):
        # Returns a 2D list of the current values in the matrix2 input fields
        values = []
        for row in self.matrix2_inputs:
            values.append([inp.text for inp in row])
        return values
    


class Matrix:
    def __init__(self,m=1,n=1):
        self.m=m
        self.n=n
        self.values=[[0 for i in range(self.n)]for j in range(self.m)]
    def set_values(self,values):
        if len(values)!=self.m:
            raise ValueError('Not right length of rows')
        else:
            for i in range(len(values)):
                if len(values[i])!=self.n:
                    raise ValueError('Not right length of columns')
                else:
                    for j in range(len(values[i])):
                        self.values[i][j]=values[i][j]
    def __str__(self):
        s=''
        for v in self.values:
            for e in v:
                s+=' '
                s+=str(e)
                s+=' '
            s+='\n'
        return s
    def multiply(self,matrix):
        # Matrix multiplication logic
        if self.n != matrix.m:
            raise ValueError("Matrix dimensions do not match for multiplication")
        result = Matrix(self.m, matrix.n)
        result.values = [[0 for _ in range(matrix.n)] for _ in range(self.m)]
        for i in range(self.m):
            for j in range(matrix.n):
                sum = 0
                for k in range(self.n):
                    sum += self.values[i][k] * matrix.values[k][j]
                result.values[i][j] = sum
        return result
            



 
app = MatrixMultiplierApp()
app.run()