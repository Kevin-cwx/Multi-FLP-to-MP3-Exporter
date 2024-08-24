using System;
using System.Diagnostics;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;
using System.Runtime.InteropServices;
using System.Threading;
using System.Windows.Forms;

class Program
{
    [DllImport("user32.dll")]
    private static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);

    [DllImport("user32.dll")]
    private static extern bool SetForegroundWindow(IntPtr hWnd);

    private const int SW_MAXIMIZE = 3;

    static void Main()
    {
        string projectPath = @"C:\Users\Kfoen\Documents\Image-Line\FL Studio\Projects\FL 21 - projects\2024\BT WIN.flp";
        string flStudioPath = @"C:\Path\To\FLStudio.exe"; // Update this path to the actual FL Studio executable path
        string screenshotPath = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.Desktop), "screenshot.png");

        // Start FL Studio with the project file
        ProcessStartInfo startInfo = new ProcessStartInfo(flStudioPath, projectPath);
        Process flStudioProcess = Process.Start(startInfo);

        // Wait for FL Studio to open (you may need to adjust the sleep time)
        Thread.Sleep(10000); // 10 seconds

        // Maximize the FL Studio window
        IntPtr hWnd = flStudioProcess.MainWindowHandle;
        ShowWindow(hWnd, SW_MAXIMIZE);
        SetForegroundWindow(hWnd);

        // Send F5 key
        SendKeys.SendWait("{F5}");

        // Wait for the rendering to complete (you may need to adjust the sleep time)
        Thread.Sleep(5000); // 5 seconds

        // Take a screenshot
        Bitmap screenshot = new Bitmap(Screen.PrimaryScreen.Bounds.Width, Screen.PrimaryScreen.Bounds.Height);
        Graphics graphics = Graphics.FromImage(screenshot);
        graphics.CopyFromScreen(0, 0, 0, 0, screenshot.Size);
        screenshot.Save(screenshotPath, ImageFormat.Png);

        Console.WriteLine("Screenshot saved to: " + screenshotPath);
    }
}
