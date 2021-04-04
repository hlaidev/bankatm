
"""
Description:

Banks stores users account. Bank API allows create user account and retrieve
account information.

For bank simulation, test account objects are stored in an array. Bank APIs are created
for future integration with real bank, possibly connected with secure cloud APIs.

User account has name, account number, and hashed password, etc.

ATM has user interface with different view state, to serve user.

AtmController class interacts with bank ATM machine to accomplish user transactions,
such as deposit and withdraw.

Simulation code is provided to exercise main scenarios.

For future integration with real bank, simple APIs to access user account are provided.
APIs to integrate ATM machine hardware are also provided. To implement ATM UI, view functions
can be overwritten.

Password is not stored in user account. salt and hash is stored for each user account. pin + salt
is used to create hash to authenticate user login.

Environment:

It is implemented with Python

To run the simulation:

python BankATM.py

"""

import hashlib, uuid

class UserAccount:
  """Define user account features."""
  def __init__(self):
    self.balance_check = 0
    self.balance_saving = 0
    self.name = ''
    self.account_number_check = ''
    self.account_number_saving = ''
    self.address = ''
    
    # Security
    self.salt = None
    self.hash = None

  def load_test_account(self):
    pass
  
  def deposit(self, acc_type, amount):
    if acc_type == 'checking':
      self.balance_check += amount
    else:
      self.balance_saving += amount

  def withdraw(self, acc_type, amount):
    if acc_type == 'checking':
      if (self.balance_check >= amount):
        self.balance_check -= amount
        return True
      else:
        return False
    else:
      if (self.balance_saving >= amount):
        self.balance_saving -= amount
        return True
      else:
        return False
  
  def balance(self):
    return self.balance

  def TODO_API_serialize_crypt(self):
    pass
  
  def TODO_API_deserialize_crypt(self):
    pass
  

class BankSimulate:
  """
  Bank stores user accounts. Bank server and ATM machine are connected with
  internet protocol. APIs will be implemented to retrieve user account information.
  """
  def __init__(self):
    # simply use checking account has key to store account object
    self.accounts = {}

  def create_account(self, account, pin):
    """Create account."""
    if not len(pin) > 4:
      return False

    account.hash, account.salt = self.hash_pass(pin)
    self.accounts[account.account_number_check] = account

  def hash_pass(self, pin, salt=None):
    # Create password
    if not salt: 
      salt = uuid.uuid4().hex
    
    return hashlib.sha512(pin + salt).hexdigest(), salt

  def get_account(self, account_number):
    return self.accounts[account_number]
    
  def auth_account(self, account, pin):
    hash, _ = self.hash_pass(pin, account.salt)
    
    #acc = self.accounts[account_number]
    if account.hash == hash:
      return account
    else:
      return None

  # TODO: future integrations.
  def API_bank_auth_account(self):
    """Account object can be serialized into json string and saved to database in future."""
    pass
  
  def API_bank_get_account(self, account_num):
    pass

  def API_bank_save_account(self):
    """Update account."""
    pass

  def API_bank_delete_account(self):
    """Delete account."""
    pass


class AtmMachine:
  """Define ATM machine behavior."""
  def __init__(self, bank):
    self.currentView = None
    self.bank = bank
    
    # ATM display to display different views.
    self.VIEW_PANEL = {
      'WELCOME': 'viewWelcome',
      'INSERT_CARD': 'viewInsertCard',
      'ENTER_PIN': 'viewEnterPin',
      'SELECT_ACCOUNT': 'viewSelectAccount',
      'BALANCE': 'viewBalance',
      'DEPOSIT': 'viewDeposit',
      'WITHDRAW': 'viewWithdraw',
      }
    self.viewWelcome()
    
  # ATM views. Print to simulate screen display
  def viewStatus(self):
    print(self.VIEW_PANEL[self.currentView])
    
  def viewWelcome(self):
    self.currentView = 'WELCOME'
    print(self.VIEW_PANEL['WELCOME'])

  def viewInsertCard(self):
    self.currentView = 'INSERT_CARD'
    print(self.VIEW_PANEL['INSERT_CARD'])

  def viewEnterPin(self):
    self.currentView = 'ENTER_PIN'
    print(self.VIEW_PANEL['ENTER_PIN'])
  
  def viewSelectAccount(self, account):
    """This view need to display account information."""
    self.currentView = 'SELECT_ACCOUNT'
    print(self.VIEW_PANEL['SELECT_ACCOUNT'])
    print('Account name: {}'.format(account.name))
  
  def viewBalance(self, balance):
    self.currentView = 'BALANCE'
    print(self.VIEW_PANEL['BALANCE'])
    print('Balance: {}'.format(balance))
  
  def viewDeposit(self, account):
    self.currentView = 'DEPOSIT'
    print(self.VIEW_PANEL['DEPOSIT'])
  
  def viewWithdraw(self, account):
    self.currentView = 'WITHDRAWs'
    print(self.VIEW_PANEL['WITHDRAWs'])


  # Event handler to handle user input of different views.
  def event_viewWelcome(self):
    pass
    
  def event_viewInsertCart(self):
    self.viewInsertCard()
    
  def event_viewEnterPin(self, acc, pin):
    """Handles event in enter pin view."""
    acc = self.bank.auth_account(acc, pin)
    
    # Go to next view of select account after successful login.
    if acc:
      self.viewSelectAccount(acc)
      print('Auth success: account={}'.format(acc.name))
    else:
      # Error handling.
      print('Auth failed! account={}'.format(acc.name))
      
  def event_viewSelectAccount(self, acc, account_type):
    """
    User select account from view account view screen. 
    Current account type needs to be stored controller.
    It goes to next view to display account balance.
    
    """
    balance = 0
    if 'checking' == account_type:
      balance = acc.balance_check
    else:
      balance = acc.balance_saving
    
    self.viewBalance(balance)

  def event_viewDeposit(self, acc, account_type, deposit_amount):
    balance = 0
    if 'checking' == account_type:
      acc.balance_check += deposit_amount
      balance = acc.balance_check
    else:
      acc.balance_saving += deposit_amount
      balance = acc.balance_saving
    
    print('Deposit: accout type={}, new balance={}'.format(account_type, balance))
  
  def event_viewWithdraw(self, acc, account_type, withdraw_amount):
    balance = 0
    status = True
    if 'checking' == account_type:
      if acc.withdraw(account_type, withdraw_amount):
        balance = acc.balance_check
      else:
        status = False
    else:
      if acc.withdraw(account_type, withdraw_amount):
        balance = acc.balance_saving
      else:
        status = False

    if status:
      print('Withdraw success. New balance={}'.format(balance))
    else:
      print('Withdraw failed due to insufficient fund. Current balance={}, withdraw={}'.format(balance, withdraw_amount))



class AtmController:
  """Interact with AtmMachine and BankSimulate class."""
  
  def __init__(self):
    self.bank = BankSimulate()
    self.atm = AtmMachine(self.bank)
    self.currentAcc = None
    self.currentAccType = 'checking'

  def simulate_create_accounts(self):
    acc = UserAccount()
    acc.balance_check = 20
    acc.balance_saving = 200
    acc.name = 'User 1'
    acc.account_number_check = '12345'
    acc.account_number_saving = '6789'
    acc.address = 'address 1'
    
    self.bank.create_account(acc, '345676')
    
    acc = UserAccount()
    acc.balance_check = 100
    acc.balance_saving = 1000
    acc.name = 'User 2'
    acc.account_number_check = '1234512345'
    acc.account_number_saving = '67896789'
    acc.address = 'address 1'
    
    self.bank.create_account(acc, '234212')

  # Simulate keyboard
  def sim_insert_card(self, account_num):
    self.atm.viewInsertCard()
    
    # Find account from bank
    self.currentAcc = self.bank.get_account(account_num)
    print('Login account: {}'.format(self.currentAcc.name))
    
  def sim_enter_pin(self, pin):
    # Display enter pin view
    self.atm.event_viewEnterPin(self.currentAcc, pin)

  def sim_select_account(self, account_type):
    self.currentAccType = account_type
    self.atm.event_viewSelectAccount(self.currentAcc, self.currentAccType)

  def sim_see_balance(self):
    self.atm.event_viewSelectAccount(self.currentAcc, self.currentAccType)

  def sim_deposit(self, deposit_amount):
    self.atm.event_viewDeposit(self.currentAcc, self.currentAccType, deposit_amount)

  def sim_withdraw(self, withdraw_amount):
    self.atm.event_viewWithdraw(self.currentAcc, self.currentAccType, withdraw_amount)


  # TODO: ATM machine hardware event, such as keyboard, or card insert.
  def notify_hardware(self, event):
    """Dispatch other hardware events."""
    pass
  
  # TODO: Future integration of user interaction with ATM machine.
  def event_insert_card(self, account_num):
    """
      # Integrate future banking API to retrieve account.
      self.currentAcc = self.bank.API_bank_get_account(account_num)
    """
    pass
    
  def event_enter_pin(self, pin):
    pass
  
  def event_select_account(self, account_type):
    pass

  def event_see_balance(self):
    pass

  def event_deposit(self):
    pass

  def event_withdraw(self):
    pass



if __name__ == "__main__":
  # Observe console output to see ATM actions.
  # Write some simulated code to validate the implementation. Unittest could be
  # used. Here is to make it simple to go through some major steps of ATM machine
  # operation to validate the implementation.
  atmControl = AtmController()

  # Create some accounts
  atmControl.simulate_create_accounts()
  
  # Demonstrate ATM functions and show its behaviors
  
  # Find account after card insert
  atmControl.sim_insert_card('1234512345')
  
  # User login with pin. After authentication, it goes to select account
  # view automatically
  atmControl.sim_enter_pin('234212')
  
  # Select account view
  atmControl.sim_select_account('saving')
  
  # Blance view
  atmControl.sim_see_balance()
  
  # Deposit $343
  atmControl.sim_deposit(343)
  
  # Withdraw $43
  atmControl.sim_withdraw(43)
  
  # Overdraw and fail.
  atmControl.sim_withdraw(43000)
