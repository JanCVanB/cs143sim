SimPy
=====

The simulation relies on SimPy for event scheduling and process management. It is possible we will use SimPy Stores as part of the Link model.

Events
------

Events are scheduled to occur at a specific time in the future.

- Send a packet
- Receive a packet
- Record simulation variables

.. note:: What other events do we have?

Processes
---------

Processes schedule events of various types and wait until the next event should be scheduled (whether a waiting for a time or an acknowledgement).

- Send data
- Update routing tables
- Monitor simulation

.. note:: What other processes do we have?

Callbacks
---------

Callbacks are actions to perform in response to an event. Any event can have callbacks for any object. Callbacks are specified when the event is scheduled.

- ???

.. note:: What callbacks do we have?
