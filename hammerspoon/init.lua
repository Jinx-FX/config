local module = {}

function module.init()
	local hyperKey = { 'alt', 'cmd' }

	-- move screen to left
	hs.hotkey.bind(hyperKey, 'h', function() hs.window.focusedWindow():moveToUnit({ 0, 0, 0.5, 1 }) end)
	-- move screen to right
	hs.hotkey.bind(hyperKey, 'l', function()
		hs.window.focusedWindow():moveToUnit({ 0.5, 0, 0.5, 1 })
	end)
	-- move screen to top
	hs.hotkey.bind(hyperKey, 'k', function()
		hs.window.focusedWindow():moveToUnit({ 0, 0, 1, 0.5 })
	end)
	-- move screen to bottom
	hs.hotkey.bind(hyperKey, 'j', function()
		hs.window.focusedWindow():moveToUnit({ 0, 0.5, 1, 0.5 })
	end)

	-- full screen, need some space to show sketchybar
	hs.hotkey.bind(hyperKey, 'f', function()
		hs.window.focusedWindow():moveToUnit({ 0, 0.037, 1, 0.963 })
	end)

	-- center screen
	hs.hotkey.bind(hyperKey, 'c', function()
		hs.window.focusedWindow():moveToUnit({ 0.2, 0.2, 0.6, 0.6 })
	end)
end

return module
