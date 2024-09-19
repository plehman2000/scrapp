# import dearpygui.dearpygui as dpg

# def save_callback():
#     spawn_window()
#     print("Save Clicked")

# dpg.create_context()
# def print_me(sender):
#     print(f"Menu Item: {sender}")
# height_window = 600
# width_window = 800

#     item.set_pos(1,1)
# dpg.create_viewport(height=600, width=600)
# dpg.setup_dearpygui()

# with dpg.viewport_menu_bar():
#     with dpg.menu(label="File"):
#         dpg.add_menu_item(label="Save", callback=print_me)
#         dpg.add_menu_item(label="Save As", callback=print_me)

#         with dpg.menu(label="Settings"):
#             dpg.add_menu_item(label="Setting 1", callback=print_me, check=True)
#             dpg.add_menu_item(label="Setting 2", callback=print_me)

#     dpg.add_menu_item(label="Help", callback=print_me)

#     with dpg.menu(label="Widget Items"):
#         dpg.add_checkbox(label="Pick Me", callback=print_me)
#         dpg.add_button(label="Press Me", callback=print_me)
#         dpg.add_color_picker(label="Color Me", callback=print_me)
            
#         with dpg.window(label="Navigation", no_move=True, height=height_window, width=width_window):
#             dpg.add_text("Hello world")
#             dpg.add_button(label="Move", callback=move_me)
#             dpg.add_input_text(label="string")
#             dpg.add_slider_float(label="float")




# dpg.show_viewport()
# dpg.start_dearpygui()
# dpg.destroy_context()


