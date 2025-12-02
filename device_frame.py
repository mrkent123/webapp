#!/usr/bin/env python3
"""
iPhone Device Frame Tool - Device Frame Application
This application creates an iPhone 14 Pro frame with a web view inside
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QPainter, QPen, QColor, QFont


class iPhoneFrameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.scale_factor = 1.0  # Default scale: 100%
        self.url = "http://localhost:5173"  # Default URL
        self.initUI()
        
    def initUI(self):
        # Set window properties
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create layout
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(50, 80, 50, 80)  # Space for phone frame
        
        # Create URL input field
        url_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setText(self.url)
        self.url_input.returnPressed.connect(self.load_url)
        
        # Create reload button
        reload_btn = QPushButton("Reload")
        reload_btn.clicked.connect(self.reload_page)
        
        url_layout.addWidget(self.url_input)
        url_layout.addWidget(reload_btn)
        layout.addLayout(url_layout)
        
        # Create web view
        self.web_view = QWebEngineView()
        self.web_view.load(QUrl(self.url))
        layout.addWidget(self.web_view)
        
        # Set initial size based on iPhone 14 Pro dimensions and scale
        self.update_size()
        
        # Set window title
        self.setWindowTitle('iPhone Device Frame')
        
    def update_size(self):
        # iPhone 14 Pro viewport: 393×852 px at DPR 3
        # Adding extra space for the device frame
        base_width = 393
        base_height = 852
        frame_thickness = 20  # Extra space for visual frame
        
        scaled_width = int((base_width + 2 * frame_thickness) * self.scale_factor)
        scaled_height = int((base_height + 2 * frame_thickness) * self.scale_factor)
        
        self.resize(scaled_width, scaled_height)
        
    def load_url(self):
        url_text = self.url_input.text()
        if not url_text.startswith(('http://', 'https://')):
            url_text = 'http://' + url_text
        self.url = url_text
        self.web_view.load(QUrl(self.url))
        
    def reload_page(self):
        self.web_view.reload()
        
    def set_scale(self, scale_percent):
        if scale_percent == 100:
            self.scale_factor = 1.0
        elif scale_percent == 120:
            self.scale_factor = 1.2
        elif scale_percent == 150:
            self.scale_factor = 1.5
        else:
            # Use provided scale percent as a multiplier
            self.scale_factor = scale_percent / 100.0
        self.update_size()
        
    def paintEvent(self, event):
        # Draw the iPhone frame
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw the outer frame
        pen = QPen(QColor(50, 50, 50), 8)
        painter.setPen(pen)
        painter.setBrush(QColor(30, 30, 30))
        
        # Calculate frame dimensions
        frame_thickness = int(20 * self.scale_factor)
        content_width = int(393 * self.scale_factor)
        content_height = int(852 * self.scale_factor)
        
        # Draw rounded rectangle for the device
        painter.drawRoundedRect(
            frame_thickness // 2, 
            frame_thickness // 2, 
            content_width + frame_thickness, 
            content_height + frame_thickness * 2, 
            20, 20
        )
        
        # Draw the screen area (inner rectangle)
        painter.setBrush(QColor(0, 0, 0))
        painter.setPen(QPen(QColor(0, 0, 0), 1))
        painter.drawRect(
            frame_thickness, 
            frame_thickness, 
            content_width, 
            content_height
        )
        
        # Draw the notch
        painter.setBrush(QColor(50, 50, 50))
        notch_width = int(100 * self.scale_factor)
        notch_height = int(20 * self.scale_factor)
        notch_x = self.width() // 2 - notch_width // 2
        # Keep notch constant size regardless of scaling to match iPhone
        notch_x = self.width() // 2 - int(100 * self.scale_factor) // 2
        notch_width = int(100 * self.scale_factor)
        painter.drawRoundedRect(notch_x, frame_thickness, notch_width, notch_height, 10, 10)


def main():
    app = QApplication(sys.argv)
    
    # Create the main window
    window = iPhoneFrameWindow()
    
    # Add keyboard shortcuts
    window.setWindowFlags(window.windowFlags() | Qt.WindowStaysOnTopHint)
    
    # Show the window
    window.show()
    
    # Set default scale to 100%
    window.set_scale(100)
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()