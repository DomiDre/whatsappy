from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import sys

this = sys.modules[__name__]
this.browser = None

def run():
  """Function to initialize webdriver and go to web.whatsapp.com"""
  this.browser = webdriver.Firefox()
  this.browser.get('https://web.whatsapp.com/')

  input("Scan QR Code with mobile Whatsapp Application and then press any key.")

def send_message(chat: str, message: str) -> bool:
  """Simple function to send 'message' to user/group 'chat'."""

  # check that the run() function has been called
  if not check_browser_initialized():
    return

  # open the chat window with given 'chat' name. If not found, return
  if not open_chat(chat):
    return
  
  # find message box, 
  # message box is div with class: <varying> copyable-text selectable-text
  # following xpath selector removes any trailing whitespaces,
  # and ignores <varying< and copyable-text of the div to
  # search for a div that has a selectable-text
  msg_box = this.browser.find_element_by_xpath(
    '//div[contains(concat(" ", normalize-space(@class), " "), '+
    '" selectable-text ")]'
  )

  # type in message
  msg_box.send_keys(message)

  # submit to chat by pressing enter
  msg_box.send_keys(webdriver.common.keys.Keys.ENTER)

### Helper Functions
def check_browser_initialized() -> bool:
  """Check if run() has been called and webdriver is initalized"""
  is_initialized = this.browser is not None
  if not is_initialized:
    print(
      "Tried to execute a command before browser was initialized. "+
      "Execute whatsappy.run() first.")
  return is_initialized

def open_chat(chat_name: str) -> bool:
  """Convenience function to open chat with user/group 'chat_name'
  
  Looks for chat_name by checking if <span> with said title can be found.
  If yes, the name is clicked and thereby the chat opened. 
  If no, an message is printed accordingly and False is returned"""
  if not check_browser_initialized():
    return
  try:
    chat = this.browser.find_element_by_xpath(f'//span[@title = "{chat_name}"]')
    chat.click()
    return True
  except NoSuchElementException:
    print(f'User/Group with name "{chat_name}" not found.')
    return False