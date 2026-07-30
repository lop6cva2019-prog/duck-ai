import threading
import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.clock import Clock

class DuckAIApp(App):
    def build(self):
        self.title = "Duck AI 🦆"
        
        # Layout chính (Dọc)
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Khung cuộn chứa tin nhắn
        self.scroll = ScrollView(size_hint=(1, 0.85))
        self.chat_history = Label(
            text="[System] Chào Gamer! Tớ là Duck AI 🦆\nBạn muốn hỏi tớ điều gì nào?\n\n",
            size_hint_y=None,
            markup=True,
            halign='left',
            valign='top'
        )
        self.chat_history.bind(texture_size=self.update_label_size)
        self.scroll.add_widget(self.chat_history)
        main_layout.add_widget(self.scroll)
        
        # Layout ô nhập & nút gửi (Ngang)
        input_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.15), spacing=5)
        
        self.user_input = TextInput(
            hint_text="Nhập câu hỏi cho Duck AI...",
            multiline=False,
            size_hint=(0.8, 1)
        )
        self.user_input.bind(on_text_validate=self.send_message)
        
        send_btn = Button(
            text="Gửi 🦆",
            size_hint=(0.2, 1),
            background_color=(0.2, 0.6, 1, 1)
        )
        send_btn.bind(on_press=self.send_message)
        
        input_layout.add_widget(self.user_input)
        input_layout.add_widget(send_btn)
        
        main_layout.add_widget(input_layout)
        return main_layout

    def update_label_size(self, instance, value):
        instance.height = value[1]
        instance.text_size = (instance.width, None)
        self.scroll.scroll_y = 0

    def append_message(self, text):
        self.chat_history.text += text + "\n\n"

    def send_message(self, instance):
        query = self.user_input.text.strip()
        if not query:
            return
            
        self.append_message(f"[b]You:[/b] {query}")
        self.user_input.text = ""
        self.append_message("[i]Duck AI đang suy nghĩ... 🦆[/i]")
        
        # Chạy kết nối AI ở thread riêng để không đơ giao diện
        threading.Thread(target=self.get_ai_response, args=(query,)).start()

    def get_ai_response(self, query):
        try:
            # Gọi API miễn phí DuckDuckGo AI / HuggingFace
            url = "https://html.duckduckgo.com/html/"
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.post(
                "https://api.duckduckgo.com/",
                data={'q': query, 'format': 'json'},
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200 and response.json().get('AbstractText'):
                reply = response.json()['AbstractText']
            else:
                reply = f"Quạc! Tớ nhận được câu hỏi '{query}' của bạn rồi nè! 🦆 Tớ là Duck AI nhí nhảnh luôn sẵn sàng hỗ trợ Gamer nha!"
        except Exception as e:
            reply = f"Quạc! Kết nối mạng hơi chậm một chút, nhưng Duck AI vẫn ở đây nè Gamer ơi! 🦆"
            
        # Cập nhật giao diện từ thread chính
        Clock.schedule_once(lambda dt: self.update_reply(reply))

    def update_reply(self, reply):
        # Xóa dòng "đang suy nghĩ" và thay bằng câu trả lời
        lines = self.chat_history.text.split("\n\n")
        if lines and "[i]Duck AI đang suy nghĩ..." in lines[-2]:
            lines.pop(-2)
        self.chat_history.text = "\n\n".join(lines)
        self.append_message(f"[b]Duck AI 🦆:[/b] {reply}")

if __name__ == "__main__":
    DuckAIApp().run()
      
