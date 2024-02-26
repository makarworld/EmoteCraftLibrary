const { app, BrowserWindow } = require('electron')
var { PythonShell } = require('python-shell');

function runServer() {

    PythonShell.run('./server.py', {mode: 'text'}, function (err, results) {
      if (err) throw err;
      // результаты - это массив, состоящий из сообщений, собранных во время выполнения
      console.log('response: ', results);
    });
  }

runServer()

function createWindow () {
  const win = new BrowserWindow({
    width: 1280,
    height: 688,
    frame: false,
    backgroundColor: '#FFF',
    webPreferences: {
        nodeIntegration: true
    }
  })

  win.loadURL('http://127.0.0.1:5010')
}

app.whenReady().then(() => {
  runServer()
  createWindow()

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow()
    }
  })
})

//Remove default menu for every new window
app.on('browser-window-created',function(e,window) {
    window.setMenu(null);
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})
