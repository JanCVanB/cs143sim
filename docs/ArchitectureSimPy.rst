SimPy
=====

The simulation relies on SimPy for event scheduling and process management. It is possible we will use SimPy Stores as part of the Link model.

Events
------

Events are scheduled to occur at a specific time in the future.

- Link available
- Packet received
- Packet added to buffer
- Send routing table update packet
- Flow starts

Processes
---------

Processes schedule events of various types and wait until the next event should be scheduled (whether a waiting for a time or an acknowledgement).

- Send data
- Update routing tables

Callbacks
---------

Callbacks are actions to perform in response to an event. Any event can have callbacks for any object. Callbacks are specified when the event is scheduled.

- Update simulation monitors
