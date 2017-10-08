The Rules of the Routing
========================

The Routing
-----------

The routing is a calculation process when the interpreter determines the next state (node) in the state diagram. Some node types provide information for this calculations, while other node types are irrelevant in this sense. The following sections will introduce the relevant ones.


Token Nodes
-----------

The *Token* node type (as its name suggests) has a key role in the routing process. It has two special variants as the *Except Token* and the *Default Token* types.

A node with *Token* type checks that the current token of the processed stream is matching to the given token class. The name of the *token class* is the value of the node. The *token class* is defined in the classifier.

For example, let define a classifier as we can see in the next code.

.. code-block:: python

    class SampleClassifier(Classifier):
        """Sample classifier"""

        @staticmethod
        def is_in_class(token_class, token):
            """Classify digits or raises error."""
            if token_class == '0-9':
                return len(token.value) == 1 and token.value.isdigit()
            else:
                raise ValueError('Invalid token class!')


The classifier returns ``True`` when the value and/or type of the current token is in the given token class, else it return with ``False`` (or raises an error in invalid cases).

We have to handle all the possible token classes in the classifier (and the invalid cases also).

The *Except Token* matches the token with the complementer class. It accepts the current token when it is not in the given token class.

The *Default Token* works like the ``default`` keyword in some programming languages. It accepts the token when the other possible nodes do not accept.


Router Notes
------------

The *Router*, *Except Router* and *Default Router* has nearly the same role as the *Token*, *Except Token* and *Default Token* types. The only difference between the router and token node types is that the token types advance the source token stream (by selecting the next token) while the router types keep the current token unchanged.


Routing Algorithm
-----------------

Let assume that we have to select the next state in the state diagram and we have more possibilities. The routing algorithm sorts the next possible states and collects the set of the reachable routing nodes. After, it tries to match the current token with all the reached nodes.

It distinguish two types of the reached states:

* *matching states*: states which accept the token,
* *default states*: states which will be accepted when there is no matching state.

The algoritm uses the following heuristic.

* When there is exactly one matching state, it will return with this state.
* When there is no matching state but there are exactly one default state, it will return with this state.
* When there is no matching or default state, it try to find the ground node.
* In other cases it raises an error, because there is no possible next state.


Ground Nodes
------------

The ground node is optional, but must be unique when given in the expression. Its purpuse is to catch the cases which cannot be handled by the explicit routes in the syntax diagram.


Expression Nodes
----------------

The nodes with *Expression* type require special consideration. The routing resolves the embedded expression.

