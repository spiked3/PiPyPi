## Contents

<span class="toctoggle"> [[hide](#)] </span></div>

*   [<span class="tocnumber">1</span> <span class="toctext">Firmware</span>](#Firmware)
*   [<span class="tocnumber">2</span> <span class="toctext">Guide</span>](#Guide)
*   [<span class="tocnumber">3</span> <span class="toctext">MQTT Bridge</span>](#MQTT_Bridge)
*   [<span class="tocnumber">4</span> <span class="toctext">API</span>](#API)

</div>

### <span class="mw-headline" id="Firmware">Firmware</span>

You will always be able to get the latest firmware here.

### <span class="mw-headline" id="Guide">Guide</span>

The API is JSON based. Commands are received and state is broadcast over the serial port.

The serial port runs at 115200, 8 bits, no parity, 1 stop bit.

All strings are JSON format {} and include a 'T' for type.

Commands sent to the Pilot will use a type of 'Cmd' {"T":"Cmd", "Cmd":"Reset"}

For broadcast the format will be;  
 {"T":"Pose", "X": 123.123456, "Y": 123.123456, "H": 123.12}

You can send a command for any broadcast type with a 'Value' of '1' or '0' to enable or disable its broadcast. If appropriate you can also specify a 'Int' value for interval. The interval is the number of 'loops' in main between broadcasts.

### <span class="mw-headline" id="MQTT_Bridge">MQTT Bridge</span>

The MQTT bridge will listen to the serial port for subscriptions. The Pilot will subscribe with 'SUB:Cmd/robot1' which causes a MQTT subscription 'Cmd/robot1/#'. This way only command topics directed at that robot will be sent via serial. The robot will broadcast JSON that includes {"Topic":"robot1"} and the bridge will use that topic as the MQTT topic.

'robot1' is the value currently used by the firmware, however it is the intent to support multiple robots by name in the future, by the year 2497.

### <span class="mw-headline" id="API">API</span>

<table class="apiTable">
<tbody>
<tr>
<th colspan="2">Commands</th>

</tr>

<tr>
<td>[Reset](/index.php?title=API:Reset&action=edit&redlink=1 "API:Reset (page does not exist)")</td>

<td>Reset robot pose, optionally specify values</td>

</tr>

<tr>
<td>[Geom](/index.php?title=API:Geom&action=edit&redlink=1 "API:Geom (page does not exist)")</td>

<td>Set robot geometry</td>

</tr>

<tr>
<td>[MMax](/index.php?title=API:MMax&action=edit&redlink=1 "API:MMax (page does not exist)")</td>

<td>Set pct of power that is actually used</td>

</tr>

<tr>
<td>[PID1](/index.php?title=API:PID1&action=edit&redlink=1 "API:PID1 (page does not exist)")</td>

<td>Set motor regulation PID values</td>

</tr>

<tr>
<td>[PID2](/index.php?title=API:PID2&action=edit&redlink=1 "API:PID2 (page does not exist)")</td>

<td>Set synchronization regulation PID values</td>

</tr>

<tr>
<td>[Rot](/index.php?title=API:Rotate&action=edit&redlink=1 "API:Rotate (page does not exist)")</td>

<td>Rotate relative or absolute</td>

</tr>

<tr>
<td>[GoTo](/index.php?title=API:GoTo&action=edit&redlink=1 "API:GoTo (page does not exist)")</td>

<td>Waypoint navigation</td>

</tr>

<tr>
<td>[Move](/index.php?title=API:MOVE&action=edit&redlink=1 "API:MOVE (page does not exist)")</td>

<td>Drive a straight line at a given +/- speed</td>

</tr>

</tbody>

</table>

<table class="apiTable">
<tbody>
<tr>
<th colspan="2">Broadcasts</th>

</tr>

<tr>
<td>[Log](/index.php?title=API:Log "API:Log")</td>

<td>System log message (eg. IEF450I, bonus points for recognizing the reference)</td>

</tr>

<tr>
<td>[Pose](/index.php?title=API:Pose&action=edit&redlink=1 "API:Pose (page does not exist)")</td>

<td>Robot State including Position</td>

</tr>

<tr>
<td>[Bump](/index.php?title=API:Bump&action=edit&redlink=1 "API:Bump (page does not exist)")</td>

<td>Bumper event</td>

</tr>

<tr>
<td>[Dest](/index.php?title=API:Dest&action=edit&redlink=1 "API:Dest (page does not exist)")</td>

<td>Destination reached event</td>

</tr>

<tr>
<td>[HeartBeat](/index.php?title=API:HB "API:HB")</td>

<td>May include additional debugging information</td>

</tr>

<tr>
<td>[Ping](/index.php?title=API:Ping&action=edit&redlink=1 "API:Ping (page does not exist)")</td>

<td>Ultrasonic threshold event</td>

</tr>

</tbody>

</table>

All Broadcast have a matching command to turn on/off the messages and set frequency

</div>