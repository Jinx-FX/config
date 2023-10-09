hyperKey = {'alt', 'cmd' }

hs.hotkey.bind(hyperKey, 'h', function() hs.window.focusedWindow():moveToUnit({0, 0, 0.5, 1}) end)
hs.hotkey.bind(hyperKey, 'l', function()
    hs.window.focusedWindow():moveToUnit({0.5, 0, 0.5, 1})
end)
hs.hotkey.bind(hyperKey, 'k', function()
    hs.window.focusedWindow():moveToUnit({0, 0, 1, 0.5})
end)
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

-- move to another screen
hs.hotkey.bind(hyperKey, 'n', function()
    hs.window.switcher.nextWindow()
end)

