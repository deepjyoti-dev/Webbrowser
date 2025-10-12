LightBrowser

A Fast, Modern, and Customizable Web Browser built with PyQt5

<!-- Optional: add a screenshot of your browser -->

Features

Tabbed Browsing: Open multiple websites in separate tabs.

Bookmarks: Save your favorite websites for quick access.

History: Keep track of visited websites.

Incognito Mode: Browse privately without saving history or cookies.

Ad-Blocking: Automatically removes common ads and pop-ups.

Download Manager: Easily download files with a file save dialog.

Dark/Light Theme Toggle: Switch between light and dark modes.

Keyboard Shortcuts:

Ctrl+T – New Tab

Ctrl+W – Close Tab

Ctrl+R – Reload Current Page

Installation

Make sure you have Python 3.8+ installed.

Install the required dependencies:

pip install PyQt5 PyQtWebEngine


Clone the repository:

git clone https://github.com/your-username/CometBrowser.git
cd CometBrowser


Run the browser:

python webbrowser.py

Usage

Open a new tab: Click the “New Tab” button or press Ctrl+T.

Close a tab: Click the close icon on the tab or press Ctrl+W.

Navigate: Type a URL in the address bar and press Enter.

Bookmarks: Click the “Bookmark” button to save a page; access saved bookmarks via the “Bookmarks” panel.

History: View visited sites using the “History” panel.

Incognito: Click “Incognito” to open a private browsing tab.

Toggle Theme: Click the “Toggle Theme” button to switch between light and dark modes.

Project Structure
CometBrowser/
│
├─ webbrowser.py         # Main application script
├─ README.md             # Project documentation
├─ screenshot.png        # Optional screenshot of the browser
└─ ...

Contributing

Contributions are welcome! If you want to add features, improve ad-blocking, or fix bugs:

Fork the repository

Create a new branch (git checkout -b feature-name)

Commit your changes (git commit -m "Add feature")

Push to the branch (git push origin feature-name)

Open a Pull Request

License

This project is licensed under the MIT License.

Future Features (Planned)

Enhanced ad-blocking using filter lists

Customizable homepage

Browser settings panel

Extensions support
