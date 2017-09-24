Node Types
==========

Properties
----------

* **source**: Does it have source node?
* **target**: Does it have target node?
* **stepping**: Does it step the source token stream to the next state by replacing the current token to the next one?
* **routing**: Does it affect the routing by checking the current token?
* **termination**: Does it terminate the parsing process?
* **parameter**: Does it have parameter?

.. csv-table::
   :header: "type", "source", "target", "stepping", "routing", "termination", "parameter"

   "start", "No", "**Yes**", "No", "No", "No", "Forbidden"
   "finish", "**Yes**", "No", "No", "**Yes**", "Depends", "Forbidden"
   "connection", "**Yes**", "**Yes**", "No", "No", "No", "Forbidden"
   "expression", "**Yes**", "**Yes**", "Depends", "**Yes**", "No", "Required"
   "ground", "No", "**Yes**", "No", "**Yes**", "No", "Forbidden"
   "token", "**Yes**", "**Yes**", "**Yes**", "**Yes**", "No", "Required"
   "except token", "**Yes**", "**Yes**", "**Yes**", "**Yes**", "No", "Required"
   "default token", "**Yes**", "**Yes**", "**Yes**", "**Yes**", "No", "Forbidden"
   "router", "**Yes**", "**Yes**", "No", "**Yes**", "No", "Required"
   "except router", "**Yes**", "**Yes**", "No", "**Yes**", "No", "Required"
   "default router", "**Yes**", "**Yes**", "No", "**Yes**", "No", "Forbidden"
   "info", "**Yes**", "**Yes**", "No", "No", "No", "Required"
   "error", "**Yes**", "**Yes**", "No", "No", "**Yes**", "Required"
   "operation", "**Yes**", "**Yes**", "No", "No", "No", "Required"
   "transformation", "**Yes**", "**Yes**", "No", "No", "No", "Required"
   "stack", "**Yes**", "**Yes**", "No", "No", "No", "Optional"
   "clean", "**Yes**", "**Yes**", "No", "No", "No", "Optional"


Details
-------

Start
~~~~~

* This node is the entry point of the expression graph.
* It must be existing and unique in any expression graph.
* It has no source side edge.
* It should not have any parameter.

.. image:: /pages/images/nodes/start.png


Finish
~~~~~~

* It is the exit point of the expression graph.
* All expression graph should contain at least one finish node.
* In the aspect of routing, it works as a default router node.
* It returns to the *caller* expression when it is not in the top level expression graph.
* It terminates the parsing process when it reached in the top level expression graph.
* It has no target side edge.
* It should not have any parameter.

.. image:: /pages/images/nodes/finish.png


Connection
~~~~~~~~~~

* Connection point for the edges.
* It has no any special meaning.
* It can helps to improve the layout of the graph.

.. image:: /pages/images/nodes/connection.png


Expression
~~~~~~~~~~

* Represents an embedded expression.
* The routing process enters to the expression for finding the next path.
* Its parameter is the name of the expression graph.

.. image:: /pages/images/nodes/expression.png


Ground
~~~~~~

* This node catches the unhandled routes of the expression graph.
* This node is not required, but must be unique in the expression when used.

.. image:: /pages/images/nodes/ground.png


Token
~~~~~

* This node matches the current token and the given token class.
* Its parameter is the name of the token class.
* It steps the source to the next token.

.. image:: /pages/images/nodes/token.png


Except Token
~~~~~~~~~~~~

* This node checks that the current node is not in the given token class.
* It steps the state of the source stream to the next token.

.. image:: /pages/images/nodes/except_token.png


Default Token
~~~~~~~~~~~~~

* This is the default case for token based routing.
* The router selects this node when the other nodes are not matching.
* It steps the state of the source stream to the next token.

.. image:: /pages/images/nodes/default_token.png


Router
~~~~~~

* This node matches the current token and the given token class.
* Its parameter is the name of the token class.
* It does not step the state of the source stream to the next token.

.. image:: /pages/images/nodes/router.png


Except Router
~~~~~~~~~~~~~

* This node checks that the current node is not in the given token class.
* It does not step the state of the source stream to the next token.

.. image:: /pages/images/nodes/except_router.png


Default Router
~~~~~~~~~~~~~~

* This is the default case for token based routing.
* The router selects this node when the other nodes are not matching.
* It does not step the state of the source stream to the next token.

.. image:: /pages/images/nodes/default_router.png


Info
~~~~

* Provides information about the current state.
* This node is useful for tracking the parsing process.
* Its parameter is the message which should be displayed.

.. image:: /pages/images/nodes/info.png


Error
~~~~~

* It signs parsing errors.
* It terminates the parsing process.
* Its parameter is the displayed error message.

.. image:: /pages/images/nodes/error.png


Operation
~~~~~~~~~

* It executes the predefined operation.
* Its parameter is the name of the operation.

.. image:: /pages/images/nodes/operation.png


Transformation
~~~~~~~~~~~~~~

* It transform the current token to an other token.
* The transformation shoud be deterministic and should not cause any side effect.
* Its parameter is the name of the transformation.

.. image:: /pages/images/nodes/transformation.png


Stack
~~~~~

* It pushes the value of the current token to the stack.
* Its parameter is the name of the stack.
* There is an *unnamed* stack which makes its parameter optional.

.. image:: /pages/images/nodes/stack.png


Clean
~~~~~

* It cleans the given stack.
* Its parameter is the name of the stack.
* There is an *unnamed* stack which makes its parameter optional.

.. image:: /pages/images/nodes/clean.png

