
from kivymd.app import MDApp
from kivymd.uix.button import *
from kivy.uix.button import Button
from kivymd.toast import toast
from kivy.uix.image import Image
from kivymd.uix.textfield import MDTextField
from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.uix.anchorlayout import MDAnchorLayout
import time
from kivy.core.window import Window
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.widget import MDWidget
import json
from kivy.uix.label import Label
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivy.storage.jsonstore import JsonStore as js
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineListItem
from screeninfo import get_monitors



# Get information about the primary monitor
primary_monitor = get_monitors()[0]

# Display the width and height of the primary monitor
screen_width = primary_monitor.width
screen_height = primary_monitor.height



try:
    with open('medical_history.json','r') as file:
        pass
        
except:
    with open('medical_history.json','w') as file:
        json.dump({},file,indent=4)

store=js('medical_history.json')

class lists(OneLineListItem):
    pass

class check_boxes(MDBoxLayout):
    pass

class medical(MDApp):
   

    def build(self):
        self.med_name=[]
        self.theme_cls.theme_style="Dark"
        return Builder.load_file('content.kv')
    
    def move_to_table(self,instance):
        print('done')
        self.root.current=self.t_s
        print('d')
        
    def on_start(self):
        
        for i in store.keys():
            self.t_s=f'_{i}_all_info'
            self.sc=f'{i}_all_info'
            med_names = [i for i in (store[i]['medicine'].keys())]
            lists=OneLineListItem(text=i,on_release=self.move_to_info,divider_color=(.9,.8,.7,0),radius=[25,25,25,25],bg_color=(.1,.2,.3,.5),text_color=(0.1,0.1,.1,1),theme_text_color='Custom')
            txt=f"""
            Date: {store[i]['date']}
            
            All your information on the date {i} are as follow


                        Your Medical condition: {store[i]['condition']}
                        
                        About your doctor:

                        name: {store[i]['medical advisor']}
                        address: {store[i]['advisor address']}
                        contact number: {store[i]['number']}
                        money charged: {store[i]['money charged']}

                        Medicines name: {str(med_names)}


            """
            print(len(self.root.ids.med.children))
            table=MDDataTable(
                
                size_hint_x=.9,
                opacity=.6,
                size_hint_y=.5,
                pos_hint={'center_x':.5,'center_y':.5},

                column_data=[
                    ('Sno',dp(30)),
                    ('Medicines',dp(30)),
                    ('before/after meal',dp(50)),
                    ('Schedule',dp(30)),
                    ('dose',dp(30))
                ],
                
                
            )

            table_screen=MDScreen(
                Image(
                        source='l.jpg',
                        allow_stretch=True,
                        opacity=.5,
                        fit_mode='fill'
                    ),
                MDAnchorLayout(
                    table,

                    anchor_x='center',
                    anchor_y='center'
                ),
                MDAnchorLayout(
                    MDIconButton(
                        text=f'{i}',
                        icon='arrow-left',
                        on_release=self.move_to_info
                    ),

                    anchor_x='left',
                    anchor_y='top'
                ),

                name=f'_{i}_all_info'
            )
            self.root.add_widget(table_screen)


            sch=[]
            
            for k in store[i]['medicine'].keys():
                med_n=store[i]['medicine'][k]['schedule']
            for l in med_n:
                if l==len(med_n):
                    sch.append(l+",")
                else:
                    sch.append(l)

            print(sch)
            sch_le=','.join(sch)
            print(sch_le)
            

            a=0
            for j in store[i]['medicine'].keys():
                a+=1
                table.add_row((a,j,store[i]['medicine'][j]['before/after meal'],sch_le,store[i]['medicine'][j]['dose']))



            
            
                

            screen=MDScreen(
                Image(
                        source='s.jpg',
                        allow_stretch=True,
                        opacity=.5,
                        fit_mode='fill'
                    ),
                MDScrollView(
                    MDBoxLayout(

                        MDLabel(
                            text=txt,
                            size_hint_x=None,
                            adaptive_height=True,
                            width=screen_width,
                            text_color=(1.0, 0.843, 0.0,1),
                            theme_text_color='Custom',
                            
                            halign='center'
                            

                        ),
                        MDRectangleFlatButton(
                            text='medical data',
                            on_release=self.move_to_table,
                            pos_hint={'center_x':.5},
                            md_bg_color= (0.5, 0.0, 1.0, 1)
                        ),
                        orientation='vertical',
                        adaptive_size=True,
                        padding=('0dp','50dp','0dp','0dp')
                    

                      

                    ),
                
                do_scroll_x=False

                ),
                MDIconButton(
                    icon='arrow-left',
                    pos_hint={'top':1},
                    on_release=self.back
                ),
                name=f'{i}_all_info'
            )

            self.root.ids.record_list.add_widget(lists)
            self.root.add_widget(screen)

            


        
            
            
            

    def move_to_info(self,instance):
        self.root.current=f'{instance.text}_all_info'

    def back(self,instance):
        self.root.current='home'
    
    def on_date_selected(self, instance, value, date_range):
        # Format the selected date as "dd month yyyy"
        date = str(value)
        formatted_date=date.replace('-','/')

        # Update the MDTextField with the formatted date
        self.root.ids.dmy.text = formatted_date
        

    def open_calendar(self):
        picker=MDDatePicker(
            title_input='Select date',
            
        )
        picker.bind(on_save=self.on_date_selected)
        picker.open()


    def checked(self):
        print('jj')
        self.c_box=check_boxes()
        if len(self.root.ids.med.children)==4:
            self.root.ids.med.remove_widget(self.root.ids.appendix_wid)
            self.root.ids.med.add_widget(self.c_box)
            self.root.ids.med.add_widget(MDWidget())
            
        
    def meal_before(self):
        self.bef_af='before meal'
        print(self.root.ids.med.children)
        

    def meal_after(self):
        self.bef_af='after meal'

    def morning(self,instance):
        
        self.boxes=self.root.ids.med.children[1]
        

    def noon(self,instance):
        self.boxes=self.root.ids.med.children[1]
        

    def evening(self,instance):
        self.boxes=self.root.ids.med.children[1]
        

    def tablets(self):
        self.dose='tablets'

    def ml(self):
        self.dose='ml'



 
    def store(self):
        try:
            with open('medical_history.json','r') as file:
                pass
        except:
            with open('medical_history.json','w') as file:
                json.dump({},file,indent=4)

        

        
        
        m_c=self.root.ids.m_c.text
        dmy=self.root.ids.dmy.text
        man=self.root.ids.man.text
        aa=self.root.ids.aa.text
        mc=self.root.ids.mc.text
        an=self.root.ids.an.text
        self.med_name.append(self.root.ids.med_name.text)
        b_a=self.bef_af
        dose=self.root.ids.dose.text
        schedule=[]


        if self.boxes.ids.check_btn3.active==True:
            schedule.append('morning')
            print('morning')
        if self.boxes.ids.check_btn4.active==True:
            schedule.append('noon')
            print('noon')
        if self.boxes.ids.check_btn5.active==True:
            schedule.append('evening/night')
            print('night')
        
        

        python_format={'condition':m_c,'date':dmy,'medical advisor':man,'advisor address':aa,'money charged':mc,'number':an,'medicine':{}}
        if m_c=='':
            path='not clear'
        elif mc=='':
            path='not clear'
        elif an=='':
            path='not clear'
        elif man=='':
            path='not clear'
        elif aa=='':
            path='not clear'
        elif dose=='':
            path='not clear'
        elif self.root.ids.med_name.text=='':
            path='not clear'
        

        elif dmy=='':
            path='not clear'
            
        else:
            path='clear'

        if path=='clear':

            for i in self.med_name:
                python_format['medicine'][i]={'before/after meal':self.bef_af,'schedule':schedule,'dose':f'{dose} {self.dose}'}

            with open('medical_history.json','r') as file:
                content=json.load(file)

            print(python_format)
            
            

            with open('medical_history.json','w') as file:
                content[dmy]=python_format
                json.dump(content,file,indent=4)

            self.bef_af=''
            schedule=[]
            self.root.ids.check_btn1.active=False
            self.root.ids.check_btn2.active=False
            self.root.ids.med.remove_widget(self.c_box)

            #clearing all the fields

           

            self.root.ids.dose.text=''

            self.boxes.ids.check_btn3.active=False
            self.boxes.ids.check_btn4.active=False
            self.boxes.ids.check_btn5.active=False
            self.root.ids.check_btn1.active=False
            self.root.ids.check_btn2.active=False
            self.root.ids.dose_ml.active=False
            self.root.ids.dose_tablets.active=False





          
            self.root.ids.med_name.text=''





            # adding the list in the data list
            self.stre=js('medical_history.json')

        else:
            toast('please first fill all fields')
            


    def all_done(self): 

        try:


            for i in self.stre.keys():
               
                if i==self.root.ids.dmy.text:
                    for i in self.stre.keys():
                        self.t_s=f'_{i}_all_info'
                        self.sc=f'{i}_all_info'
                        meds_names = [i for i in (store[i]['medicine'].keys())]

                        lists=OneLineListItem(text=i,on_release=self.move_to_info,divider_color=(.9,.8,.7,0),radius=[25,25,25,25],bg_color=(.1,.2,.3,.5),text_color=(0.1,0.1,.1,1),theme_text_color='Custom')
                        txt=f"""
                        Date: {self.stre[i]['date']}
                        
                        All your information on the date {i} are as follow


                                    Your Medical condition: {self.stre[i]['condition']}
                                    
                                    About your doctor:

                                    name: {self.stre[i]['medical advisor']}
                                    address: {self.stre[i]['advisor address']}
                                    contact number: {self.stre[i]['number']}
                                    money charged: {self.stre[i]['money charged']}

                                    Medicines name: {meds_names}


                        """
                        print(len(self.root.ids.med.children))
                        table=MDDataTable(
                            
                            size_hint_x=.9,
                            opacity=.6,
                            size_hint_y=.5,
                            pos_hint={'center_x':.5,'center_y':.5},

                            column_data=[
                                ('Sno',dp(30)),
                                ('Medicines',dp(30)),
                                ('before/after meal',dp(50)),
                                ('Schedule',dp(30)),
                                ('dose',dp(30))
                            ],
                            
                            
                        )

                        table_screen=MDScreen(
                            Image(
                                    source='l.jpg',
                                    allow_stretch=True,
                                    opacity=.5,
                                    fit_mode='fill'
                                ),
                            MDAnchorLayout(
                                table,

                                anchor_x='center',
                                anchor_y='center'
                            ),
                            MDAnchorLayout(
                                MDIconButton(
                                    icon='arrow-left',
                                    on_release=self.move_to_info
                                ),

                                anchor_x='left',
                                anchor_y='top'
                            ),

                            name=f'_{i}_all_info'
                        )
                        self.root.add_widget(table_screen)


                        sch=[]
                        
                        for k in self.stre[i]['medicine'].keys():
                            med_n=self.stre[i]['medicine'][k]['schedule']
                        for l in med_n:
                            if l==len(med_n):
                                sch.append(l+",")
                            else:
                                sch.append(l)

                        print(sch)
                        sch_le=','.join(sch)
                        print(sch_le)
                        

                        a=0
                        for j in self.stre[i]['medicine'].keys():
                            a+=1
                            table.add_row((a,j,self.stre[i]['medicine'][j]['before/after meal'],sch_le,self.stre[i]['medicine'][j]['dose']))



                        
                        
                            

                        screen=MDScreen(
                            Image(
                                    source='s.jpg',
                                    allow_stretch=True,
                                    opacity=.5,
                                    fit_mode='fill'
                                ),
                            MDScrollView(
                                MDBoxLayout(

                                    MDLabel(
                                        text=txt,
                                        size_hint_x=None,
                                        adaptive_height=True,
                                        width=screen_width,
                                        text_color=(1.0, 0.843, 0.0,1),
                                        theme_text_color='Custom',
                                        
                                        halign='center'
                                        

                                    ),
                                    MDRectangleFlatButton(
                                        text='medical data',
                                        on_release=self.move_to_table,
                                        pos_hint={'center_x':.5},
                                        md_bg_color= (0.5, 0.0, 1.0, 1)
                                    ),
                                    orientation='vertical',
                                    adaptive_size=True,
                                    padding=('0dp','50dp','0dp','0dp')
                                

                                

                                ),
                            
                            do_scroll_x=False

                            ),
                            MDIconButton(
                                icon='arrow-left',
                                pos_hint={'top':1},
                                on_release=self.back
                            ),
                            name=f'{i}_all_info'
                        )

                        self.root.ids.record_list.add_widget(lists)
                        self.root.add_widget(screen)


                    
                    self.root.ids.mc.text=''
                    self.root.ids.an.text=''

                    self.root.ids.man.text=''

                    self.root.ids.dose.text=''
                    self.root.ids.dmy.text=''

                    

                    self.root.ids.m_c.text=''

                    self.root.ids.aa.text=''
                    self.root.ids.med_name.text=''
                    self.boxes.ids.check_btn3.active=False
                    self.boxes.ids.check_btn4.active=False
                    self.boxes.ids.check_btn5.active=False
                    self.root.ids.check_btn1.active=False
                    self.root.ids.check_btn2.active=False
                    self.root.ids.dose_ml.active=False
                    self.root.ids.dose_tablets.active=False
                    self.med_name=[]

                    a=0
                    print('his also')
                
                else:
                    print('nope')
        except:
            toast('please first fill all the felds')





            
            
                
medical().run()
