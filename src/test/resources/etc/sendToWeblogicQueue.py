# Java Message Service - Queue Sender
#
# JMS objects are looked up and messages are created once during
# initialisation. This default JNDI names are for the WebLogic Server
# 7.0 examples domain - change accordingly.
#
# Each worker thread:
#  - Creates a queue session
#  - Sends ten messages
#  - Closes the queue session

from net.grinder.script.Grinder import grinder
from net.grinder.script import Test
from jarray import zeros
from java.util import Properties, Random
from javax.jms import Session
from javax.naming import Context, InitialContext
from weblogic.jndi import WLInitialContextFactory

# Look up connection factory and queue in JNDI.
properties = Properties()

# I N S E R T   Y O U R   W E B L O G I C   U R L    H E R E
properties[Context.PROVIDER_URL] = "t3://ifappd104d-v01t:9001"

properties[Context.INITIAL_CONTEXT_FACTORY] = WLInitialContextFactory.name
properties[Context.SECURITY_PRINCIPAL] = "weblogic"
properties[Context.SECURITY_CREDENTIALS] = "weblogic"

initialContext = InitialContext(properties)

# I N S E R T    Y O U R   C O N N E C T I O N   F A C T O R Y   N A M E
connectionFactory = initialContext.lookup("Fabric.Jms.ConnectionFactory")

# I N S E R T    Y O U R   Q U E U E   N A M E
queue = initialContext.lookup("queue.Fabric.Exception")
initialContext.close()

# Create a connection.
connection = connectionFactory.createQueueConnection()
connection.start()

random = Random()

def createTextMessage(session):
   linestring = open('TestEvent.xml', 'r').read()
   message = session.createTextMessage(linestring)

   return message


def createBytesMessage(session, size):
    bytes = zeros(size, 'b')
    random.nextBytes(bytes)
    message = session.createBytesMessage()
    message.writeBytes(bytes)
    return message

class TestRunner:
    def __call__(self):
        log = grinder.logger.output

        log("Creating queue session")
        session = connection.createQueueSession(0, Session.AUTO_ACKNOWLEDGE)

        sender = session.createSender(queue)
        instrumentedSender = Test(1, "Send a message").wrap(sender)

        message = createTextMessage(session)

        log("Sending ten messages")

        for i in range(0, 10):
            instrumentedSender.send(message)
            grinder.sleep(100)

        log("Closing queue session")
        session.close()
