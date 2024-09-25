local wezterm = require 'wezterm'

wezterm.log_info('Config file ' .. wezterm.config_file)

local config = wezterm.config_builder()
config.default_prog = { 'powershell.exe' }
config.default_cwd = "C:\\GH\\scrapp\\"
-- This is where you actually apply your config choices

-- For example, changing the color scheme:
config.color_scheme = 'Teerb'

-- Configure initial window size
config.initial_cols = 120
config.initial_rows = 30

-- Function to send a command and execute it
local function send_command(pane, command)
  pane:send_text(command .. "\n")
end

-- Set up the initial layout and spawn panes on startup
wezterm.on("gui-startup", function(cmd)
  local tab, pane, window = wezterm.mux.spawn_window(cmd or {})
  
--   pane.send_command("conda activate q")
  -- Split the window vertically
  local pane2 = pane:split({ direction = "Right"})
  
  -- Split the right pane horizontally
  local pane3 = pane2:split({ direction = "Bottom" })
  
  -- Run commands in each pane
--   send_command(pane, "conda activate q")
--   send_command(pane2, "C:\\Users\\Patrick\\AppData\\Local\\Programs\\Ollama\\ollama serve")
--   send_command(pane3, "streamlit run scrapp.py")
end)

return config