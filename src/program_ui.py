'''
Created on 23.12.2015

@author: Christopher Skerra, Dennis Skerra
@contact: Skerra.Christopher@yahoo.de

Licensed under CC BY-NC-SA 4.0
https://creativecommons.org/licenses/by-nc-sa/4.0/

'''

import Tkinter
import os # needed for relative image paths

class ProgramUI(object):

    def __init__(self, root):
        
        # initial directory for file dialogs
        self.lastdirectory = os.getcwd()
        
        # Component Inits
        self.middle_controls_frame = Tkinter.Frame(root,)
        
        self.debug_text = Tkinter.Text(root,
            height = 1,
            state = "disabled",
            width = 1,
        )
       
        # Dataset listbox UI Elements
        self.item_list = Tkinter.Listbox(root,
            activestyle = "dotbox",
            height = 1,
            setgrid = 1,
            width = 01,
            selectmode="SINGLE"
        )
        self.add_button = Tkinter.Button(root,
            text = "Add",
        )
        self.remove_button = Tkinter.Button(root,
            text = "Remove",
        )
        
        # Dataset Management UI Elements
        self._label_Datasetmgt = Tkinter.Label(self.middle_controls_frame,
            text = "Dataset management",
        )
        self.reset_dataset_button = Tkinter.Button(self.middle_controls_frame,
            text = "Reset dataset",
        )
        self.revert_button = Tkinter.Button(self.middle_controls_frame,
            text = "Revert one step",
        )
        
        # Plotting Dataset UI Elements
        self._label_Plotting = Tkinter.Label(self.middle_controls_frame,
            text = "Plot dataset",
        )        
        self.plot_mean_button = Tkinter.Button(self.middle_controls_frame,
            text = "Mean Unspiked",
        )      
        self.plot_original_button = Tkinter.Button(self.middle_controls_frame,
            text = "Original",
        )
        self.plot_unspiked_button = Tkinter.Button(self.middle_controls_frame,
            text = "Unspiked",
        )        

        # Export Dataset UI Elements
        self._label_Export = Tkinter.Label(self.middle_controls_frame,
            text = "Export dataset",
        )
        self.export_mean_button = Tkinter.Button(self.middle_controls_frame,
            text = "Mean unspiked",
        )
        self.export_csv_button = Tkinter.Button(self.middle_controls_frame,
            text = "Unspiked as CSV",
        )
        
        # Unspiking Dataset UI Elements
        self._label_Unspiking = Tkinter.Label(self.middle_controls_frame,
            text = "Unspiking functions",
        )
        self.run_unspike_button = Tkinter.Button(self.middle_controls_frame,
            text = "Run Unspike",
        )
        self.dryrun_button = Tkinter.Button(self.middle_controls_frame,
            text = "Dryrun",
        )
        self.manual_unspiker_button = Tkinter.Button(self.middle_controls_frame,
            text = "Manual unspiker",
        )     

        self.mindistmean_label = Tkinter.Label(self.middle_controls_frame,
            text = "Min dist. from mean",
        )
        self.mindistmean_entry = Tkinter.Entry(self.middle_controls_frame,
            width = 1,
        )
        self.mindistmean_entry.insert(0, "100")
        
        self.Trendlinedegree_label = Tkinter.Label(self.middle_controls_frame,
            text = "Trendline degree",
        )
        self.trendlinedegree_entry = Tkinter.Entry(self.middle_controls_frame,
            width = 1,
        )
        self.trendlinedegree_entry.insert(0, "90")
        
        self.useTrendlinevariable = Tkinter.IntVar()
        self.enableTrendline_checkbox = Tkinter.Checkbutton(self.middle_controls_frame, 
            text="Use trendline",variable=self.useTrendlinevariable
        )
        self.enableTrendline_checkbox.select()        
       
        self.disterrfactor_label = Tkinter.Label(self.middle_controls_frame,
            text = "Distance error factor",
        )
        self.disterrfactor_entry = Tkinter.Entry(self.middle_controls_frame,
            width = 1,
        )
        self.disterrfactor_entry.insert(0, "3")
        
        # Dataset information UI Elements
        self.datainfo_label = Tkinter.Label(root,
            text = "Dataset information",
        )
        self.infobox_text = Tkinter.Text(root,
            height = 1,
            state = "disabled",
            width = 1,
        )

        # widget commands
        self.item_list.bind('<<ListboxSelect>>', self.immediately)

        # Dataset listbox buttons
        self.add_button.configure(
            command = self.add_button_command
        )
        self.remove_button.configure(
            command = self.remove_button_command
        )
        
        # Dataset Management Buttons Binding
        self.reset_dataset_button.configure(
            command = self.reset_dataset_button_command
        )
        self.revert_button.configure(
            command = self.revert_button_command
        )
        
        # Unspike Buttons Binding        
        self.run_unspike_button.configure(
            command = self.run_unspike_button_command
        )
        self.dryrun_button.configure(
            command = self.dryrun_button_command
        )
        self.manual_unspiker_button.configure(
            command = self.manual_unspiker_button_command
        )

        # Export Buttons Binding
        self.export_mean_button.configure(
            command = self.export_mean_button_command
        )
        self.export_csv_button.configure(
            command = self.export_csv_button_command
        )
        
        # Plot Buttons Bindings
        self.plot_original_button.configure(
            command = self.plot_original_button_command
        )
        self.plot_unspiked_button.configure(
            command = self.plot_unspiked_button_command
        ) 
        self.plot_mean_button.configure(
            command = self.plot_mean_button_command
        )

        # Layout Configurations
        self.middle_controls_frame.grid(
            in_    = root,
            column = 3,
            row    = 1,
            columnspan = 1,
            ipadx = 0,
            ipady = 0,
            padx = 0,
            pady = 0,
            rowspan = 4,
            sticky = "news"
        )
        self.debug_text.grid(
            in_    = root,
            column = 1,
            row    = 5,
            columnspan = 5,
            ipadx = 0,
            ipady = 0,
            padx = 0,
            pady = 0,
            rowspan = 1,
            sticky = "news"
        )
        # listbox UI elements configurations
        self.item_list.grid(
            in_    = root,
            column = 1,
            row    = 2,
            columnspan = 2,
            ipadx = 0,
            ipady = 0,
            padx = 0,
            pady = 0,
            rowspan = 3,
            sticky = "nsew"
        )
        self.add_button.grid(
            in_    = root,
            column = 1,
            row    = 1,
            columnspan = 1,
            ipadx = 0,
            ipady = 0,
            padx = 0,
            pady = 0,
            rowspan = 1,
            sticky = "nsew"
        )
        self.remove_button.grid(
            in_    = root,
            column = 2,
            row    = 1,
            columnspan = 1,
            ipadx = 0,
            ipady = 0,
            padx = 0,
            pady = 0,
            rowspan = 1,
            sticky = "nsew"
        )
        # Datasetmgt configurations
        self._label_Datasetmgt.grid(
            in_    = self.middle_controls_frame,
            column = 1,
            row    = 1,
            columnspan = 2,
            ipadx = 0,
            ipady = 0,
            padx = 0,
            pady = 0,
            rowspan = 1,
            sticky = "nsew"
        )
        self.reset_dataset_button.grid(
            in_    = self.middle_controls_frame,
            column = 1,
            row    = 2,
            columnspan = 1,
            ipadx = 0,
            ipady = 0,
            padx = 0,
            pady = 0,
            rowspan = 1,
            sticky = "nsew"
        )
        self.revert_button.grid(
            in_    = self.middle_controls_frame,
            column = 2,
            row    = 2,
            columnspan = 1,
            ipadx = 0,
            ipady = 0,
            padx = 0,
            pady = 0,
            rowspan = 1,
            sticky = "nsew"
        )
        # Plotting UI Elements configurations
        self._label_Plotting.grid(
            in_    = self.middle_controls_frame,
            column = 1,
            row    = 3,
            columnspan = 2,
            ipadx = 0,
            ipady = 0,
            padx = 0,
            pady = 0,
            rowspan = 1,
            sticky = "nsew"
        )
        self.plot_original_button.grid(
            in_    = self.middle_controls_frame,
            column = 1,
            row    = 4,
            columnspan = 1,
            ipadx = 0,
            ipady = 0,
            padx = 0,
            pady = 0,
            rowspan = 1,
            sticky = "nsew"
        )        
        self.plot_mean_button.grid(
            in_    = self.middle_controls_frame,
            column = 1,
            row    = 5,
            columnspan = 1,
            ipadx = 0,
            ipady = 0,
            padx = 0,
            pady = 0,
            rowspan = 1,
            sticky = "nsew"
        )
        self.plot_unspiked_button.grid(
            in_    = self.middle_controls_frame,
            column = 2,
            row    = 4,
            columnspan = 1,
            ipadx = 0,
            ipady = 0,
            padx = 0,
            pady = 0,
            rowspan = 1,
            sticky = "nsew"
        )
        # Export UI Elements configurations
        self._label_Export.grid(
            in_    = self.middle_controls_frame,
            column = 1,
            row    = 6,
            columnspan = 2,
            ipadx = 0,
            ipady = 0,
            padx = 0,
            pady = 0,
            rowspan = 1,
            sticky = "nsew"
        )
        self.export_csv_button.grid(
            in_    = self.middle_controls_frame,
            column = 1,
            row    = 7,
            columnspan = 1,
            ipadx = 0,
            ipady = 0,
            padx = 0,
            pady = 0,
            rowspan = 1,
            sticky = "nsew"
        )
        self.export_mean_button.grid(
            in_    = self.middle_controls_frame,
            column = 2,
            row    = 7,
            columnspan = 1,
            ipadx = 0,
            ipady = 0,
            padx = 0,
            pady = 0,
            rowspan = 1,
            sticky = "nsew"
        )
        # Unspike UI Elements configurations    
        self._label_Unspiking.grid(
            in_    = self.middle_controls_frame,
            column = 1,
            row    = 8,
            columnspan = 2,
            ipadx = 0,
            ipady = 0,
            padx = 0,
            pady = 0,
            rowspan = 1,
            sticky = "nsew"
        )
        self.mindistmean_label.grid(
            in_    = self.middle_controls_frame,
            column = 1,
            row    = 9,
            columnspan = 1,
            ipadx = 0,
            ipady = 0,
            padx = 0,
            pady = 0,
            rowspan = 1,
            sticky = ""
        )
        self.mindistmean_entry.grid(
            in_    = self.middle_controls_frame,
            column = 2,
            row    = 9,
            columnspan = 1,
            ipadx = 0,
            ipady = 0,
            padx = 0,
            pady = 0,
            rowspan = 1,
            sticky = "ew"
        )
        self.disterrfactor_label.grid(
            in_    = self.middle_controls_frame,
            column = 1,
            row    = 10,
            columnspan = 1,
            ipadx = 0,
            ipady = 0,
            padx = 0,
            pady = 0,
            rowspan = 1,
            sticky = ""
        )
        self.disterrfactor_entry.grid(
            in_    = self.middle_controls_frame,
            column = 2,
            row    = 10,
            columnspan = 1,
            ipadx = 0,
            ipady = 0,
            padx = 0,
            pady = 0,
            rowspan = 1,
            sticky = "ew"
        )        
        self.Trendlinedegree_label.grid(
            in_    = self.middle_controls_frame,
            column = 1,
            row    = 11,
            columnspan = 1,
            ipadx = 0,
            ipady = 0,
            padx = 0,
            pady = 0,
            rowspan = 1,
            sticky = ""
        )
        self.trendlinedegree_entry.grid(
            in_    = self.middle_controls_frame,
            column = 2,
            row    = 11,
            columnspan = 1,
            ipadx = 0,
            ipady = 0,
            padx = 0,
            pady = 0,
            rowspan = 1,
            sticky = "ew"
        )
        self.enableTrendline_checkbox.grid(
            in_    = self.middle_controls_frame,
            column = 1,
            row    = 12,
            columnspan = 1,
            ipadx = 0,
            ipady = 0,
            padx = 0,
            pady = 0,
            rowspan = 1,
            sticky = "ew"
        )
        self.run_unspike_button.grid(
            in_    = self.middle_controls_frame,
            column = 1,
            row    = 13,
            columnspan = 1,
            ipadx = 0,
            ipady = 0,
            padx = 0,
            pady = 0,
            rowspan = 1,
            sticky = "nsew"
        )
        self.dryrun_button.grid(
            in_    = self.middle_controls_frame,
            column = 2,
            row    = 13,
            columnspan = 1,
            ipadx = 0,
            ipady = 0,
            padx = 0,
            pady = 0,
            rowspan = 1,
            sticky = "nsew"
        ) 
        self.manual_unspiker_button.grid(
            in_    = self.middle_controls_frame,
            column = 1,
            row    = 14,
            columnspan = 2,
            ipadx = 0,
            ipady = 0,
            padx = 0,
            pady = 0,
            rowspan = 1,
            sticky = "nsew"
        )
        
        # data information configurations              
        self.datainfo_label.grid(
            in_    = root,
            column = 4,
            row    = 1,
            columnspan = 1,
            ipadx = 0,
            ipady = 0,
            padx = 0,
            pady = 0,
            rowspan = 1,
            sticky = "sw"
        )
        self.infobox_text.grid(
            in_    = root,
            column = 4,
            row    = 2,
            columnspan = 2,
            ipadx = 0,
            ipady = 0,
            padx = 0,
            pady = 0,
            rowspan = 3,
            sticky = "news"
        )
        
        # Resize Behavior
        root.grid_rowconfigure(1, weight = 0, minsize = 0, pad = 0)
        root.grid_rowconfigure(2, weight = 3, minsize = 0, pad = 0)
        root.grid_rowconfigure(3, weight = 0, minsize = 0, pad = 0)
        root.grid_rowconfigure(4, weight = 1, minsize = 0, pad = 0)
        root.grid_rowconfigure(5, weight = 1, minsize = 0, pad = 0)
        root.grid_columnconfigure(1, weight = 1, minsize = 0, pad = 0)
        root.grid_columnconfigure(2, weight = 1, minsize = 0, pad = 0)
        root.grid_columnconfigure(3, weight = 0, minsize = 0, pad = 0)
        root.grid_columnconfigure(4, weight = 2, minsize = 0, pad = 0)
        root.grid_columnconfigure(5, weight = 2, minsize = 0, pad = 0)
        self.middle_controls_frame.grid_rowconfigure(1, weight = 0, minsize = 2, pad = 0)
        self.middle_controls_frame.grid_rowconfigure(2, weight = 0, minsize = 2, pad = 0)
        self.middle_controls_frame.grid_rowconfigure(3, weight = 0, minsize = 2, pad = 0)
        self.middle_controls_frame.grid_rowconfigure(4, weight = 0, minsize = 2, pad = 0)
        self.middle_controls_frame.grid_rowconfigure(5, weight = 0, minsize = 2, pad = 0)        
        self.middle_controls_frame.grid_rowconfigure(6, weight = 0, minsize = 2, pad = 0)
        self.middle_controls_frame.grid_rowconfigure(7, weight = 0, minsize = 2, pad = 0)
        self.middle_controls_frame.grid_rowconfigure(8, weight = 0, minsize = 2, pad = 0)
        self.middle_controls_frame.grid_rowconfigure(9, weight = 0, minsize = 2, pad = 0)
        self.middle_controls_frame.grid_rowconfigure(10, weight = 0, minsize = 2, pad = 0)
        self.middle_controls_frame.grid_rowconfigure(11, weight = 0, minsize = 2, pad = 0)
        self.middle_controls_frame.grid_rowconfigure(12, weight = 0, minsize = 2, pad = 0)
        self.middle_controls_frame.grid_rowconfigure(13, weight = 0, minsize = 2, pad = 0)
        self.middle_controls_frame.grid_rowconfigure(14, weight = 0, minsize = 2, pad = 0)
        self.middle_controls_frame.grid_rowconfigure(15, weight = 0, minsize = 2, pad = 0)

        self.middle_controls_frame.grid_columnconfigure(1, weight = 0, minsize = 40, pad = 0)
        self.middle_controls_frame.grid_columnconfigure(2, weight = 0, minsize = 40, pad = 0)
        self.debug_text.tag_config("e", background="yellow",  foreground="red")


