from html import entities
import dearpygui.dearpygui as dpg
import premiser

WINDOW_SIZE_HW = [900,1300]

global REWRITE_PROMPT
REWRITE_PROMPT = False
dpg.create_context()

with dpg.theme() as global_theme:

    with dpg.theme_component(dpg.mvAll):
        # dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (52, 235, 186, 100),   category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 3, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 6, category=dpg.mvThemeCat_Core)

    # with dpg.theme_component(dpg.mvInputText):
    #     dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (140, 255, 23), category=dpg.mvThemeCat_Core)
    #     dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)

dpg.bind_theme(global_theme)


# dpg.show_style_editor()

def prompt_entered_callback():
    conclusion = dpg.get_value("prompt_input")
    if REWRITE_PROMPT:
        conclusion = premiser.rewrite_conclusion(conclusion)
    dpg.add_text("Conclusion", parent="start_window")
    dpg.add_text(conclusion, parent="start_window")

    
    entities = premiser.get_entities(conclusion)
    for ent in entities:
        dpg.add_text(ent[0] + ": " + ent[1] + "\n", parent="start_window")
    premiser.premise_flow_dpg()

def rewrite_prompt_callback():
    global REWRITE_PROMPT
    REWRITE_PROMPT = not REWRITE_PROMPT

    
dpg.create_viewport(width=WINDOW_SIZE_HW[1], height=WINDOW_SIZE_HW[0])
dpg.setup_dearpygui()

with dpg.window(tag="start_window",label="Start Window", pos=[0,0], width=WINDOW_SIZE_HW[1]//4 , height=WINDOW_SIZE_HW[0]):
    dpg.add_text("Enter a claim")
    dpg.add_input_text(tag="prompt_input", callback=prompt_entered_callback, on_enter=True,  width=300, height=100)
    dpg.add_checkbox(tag="prompt_rewrite_checkbox", label="Optimize prompt", callback=rewrite_prompt_callback)
dpg.show_viewport()
dpg.start_dearpygui()   
dpg.destroy_context()