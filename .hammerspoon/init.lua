hyperKey = {'alt', 'cmd' }

-- move screen to left
hs.hotkey.bind(hyperKey, 'h', function() hs.window.focusedWindow():moveToUnit({0, 0, 0.5, 1}) end)
-- move screen to right
hs.hotkey.bind(hyperKey, 'l', function()
    hs.window.focusedWindow():moveToUnit({0.5, 0, 0.5, 1})
end)
-- move screen to top
hs.hotkey.bind(hyperKey, 'k', function()
    hs.window.focusedWindow():moveToUnit({0, 0, 1, 0.5})
end)
-- move screen to bottom
hs.hotkey.bind(hyperKey, 'j', function()
    hs.window.focusedWindow():moveToUnit({0, 0.5, 1, 0.5})
end)

-- full screen
hs.hotkey.bind(hyperKey, 'f', function()
    hs.window.focusedWindow():moveToUnit({0, 0, 1, 1})
end)

-- center screnn
hs.hotkey.bind(hyperKey, 'c', function()
    hs.window.focusedWindow():moveToUnit({0.2, 0.2, 0.6, 0.6})
end)

-- move to previous screen
hs.hotkey.bind(hyperKey, 'm', function()
		hs.window.switcher.previousWindow()
end)

-- move to next screen
hs.hotkey.bind(hyperKey, 'n', function()
    hs.window.switcher.nextWindow()
end)

