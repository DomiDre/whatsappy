from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import sys, re, datetime
from dataclasses import dataclass

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
  # could however be multiple... smiles have similar signature
  msg_box_candidates = this.browser.find_elements_by_xpath(
    '//div[contains(concat(" ", normalize-space(@class), " "), '+
    '" selectable-text ")]'
  )

  msg_box = None
  for element in msg_box_candidates:
    if element.get_attribute('contenteditable'):
      msg_box = element
      break
  if msg_box is None:
    return

  # type in message
  msg_box.send_keys(message)

  # submit to chat by pressing enter
  msg_box.send_keys(webdriver.common.keys.Keys.ENTER)

def read_messages(minimal_timestamp=0):
  main_element = this.browser.find_element_by_id('main')
  chat_elements = main_element.find_elements_by_xpath('div/div/div/div/div')
  chat_elements.reverse()
  for chat_element in chat_elements:
    chatbox = identify_chat_element(chat_element)

    if chatbox:
      if chatbox.timestamp < minimal_timestamp:
        break
      print(chatbox.timestamp, chatbox.sender, chatbox.message)


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

def read_source_code() -> str:
  """Get the source code of the current view"""
  return this.browser.page_source

def get_new_messages():
  """Read new messages from all groups/users that were received"""

  # Find users/groups where a little number is on the screen
  number_pattern = re.compile(r"\d+")
  candidates = this.browser.find_elements_by_xpath('//div/span/div/span')

  new_message_elements = []
  for element in candidates:
    match = number_pattern.match(element.text)
    if match:
      new_message_elements.append(new_message_elements)
  
  if len(new_message_elements) == 0:
    return

  # evaluate all users/groups in new_message_elements

  # TODO

@dataclass
class ChatBox:
  sender: str
  timestamp: int
  message: str
  is_incoming_message: bool

def identify_chat_element(chat_element):
  is_incoming_message = False
  chat_element_class = chat_element.get_attribute('class')
  if 'message-in' in chat_element_class:
    is_incoming_message = True
  elif 'message-out'   in chat_element_class:
    is_incoming_message = False
  else:
    return

  try:
    chat_childs = chat_element.find_elements_by_xpath('div/div/div/div')
  except NoSuchElementException:
    return

  text_containing_child = None
  timestamp_name = None
  for chat_child in chat_childs:
    timestamp_name = chat_child.get_attribute('data-pre-plain-text')
    if timestamp_name:
      text_containing_child = chat_child
      break
  
  if text_containing_child is None:
    return

  chat_text = None
  try:
    chat_text = text_containing_child.find_element_by_xpath('div/span/span')
  except NoSuchElementException:
    return

  message = chat_text.text
  
  matchObj = re.match(
    r'\[(\d{2}:\d{2}), (\d+.\d+.\d+)\] (\D+):',
    timestamp_name
  )

  time = matchObj.group(1)
  date = matchObj.group(2)
  sender = matchObj.group(3)
  timestamp = datetime.datetime.strptime(
    date + ' ' + time, '%d.%m.%Y %H:%M'
  ).timestamp()
  chatbox = ChatBox(sender, timestamp, message, is_incoming_message)

  return chatbox