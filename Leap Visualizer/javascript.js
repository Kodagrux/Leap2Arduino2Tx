var output = document.getElementById('output');
var frameString = "", handString = "", fingerStrign = "";
var hand, finger;

var lefthand = righthand = false;
var cube = document.getElementById('cube');
var yaw, pitch, roll, lheight; //current values
var yaw2, pitch2, roll2, lheight2; //new values

var sluggish = false;

//Leap controller loop 
var options = {enableGestures: true};


//Main Leep Loop
Leap.loop(options, function(frame) {
	frameString = concatData("frame_id", frame.id);
	frameString += concatData("num_hands", frame.hands.length);
	frameString += concatData("num_fingers", frame.fingers.length);
	frameString += "<br>";

	
	//Loops over the hands
	for (var i = 0, len = frame.hands.length; i < len; i++) {
		hand = frame.hands[i];
		handString = concatData("hand_type", hand.type);

		if (hand.type == "right" && hand.grabStrength < 0.8 && hand.confidence > 0.3) {
			roll2 = hand.roll();
			pitch2 = hand.pitch();
			yaw2 = hand.yaw();
			righthand = true;
		} else {
			righthand = false;
		}

		if (hand.type == "left" && hand.grabStrength < 0.8 && hand.confidence > 0.3) {
			lefthand = true;
			lheight2 = hand.palmPosition[1];
		} else {
			lefthand = false;
		}

		opacityControll();
		cubeControll();

		handString += concatData("hand_roll", hand.roll());
		handString += concatData("hand_pitch", hand.pitch());
		handString += concatData("hand_yaw", hand.yaw());
		handString += concatData("pinch_strength", hand.pinchStrength);
		handString += concatData("grab_strength", hand.grabStrength);
		handString += concatData("hand_height", hand.palmPosition[1]);
		handString += concatData("confidence", hand.confidence);
		frameString += handString;
		frameString += "<br>";

		//Loops over the fingers
		/*for (var j = 0, len2 = hand.fingers.length; j < len2; j++) {
			finger = hand.fingers[j];
			fingerString = concatData("finger_type" + " (" + finger.type + ")", getFingerName(finger.type));

			//De olika jointarna för fingrarna
			fingerString += concatJointPosition("finger_dip", finger.dipPosition); //Längst ut jointen
			fingerString += concatJointPosition("finger_pip", finger.pipPosition); //Mitten jointen
			fingerString += concatJointPosition("finger_mcp", finger.mcpPosition); //Knogen

			frameString += fingerString;
			frameString += "<br>";
		}*/

	}

	if (!righthand || frame.hands.length == 0) {
		righthand = false;
		roll2 = valueReset(roll, 0, 0.03);
		pitch2 = valueReset(pitch, 0, 0.03);
		yaw2 = valueReset(yaw, 0, 0.03);
		cubeControll();
	} 

	if (!lefthand || frame.hands.length == 0) {
		lefthand = false;
		lheight2 = valueReset(lheight2, 215, 2);
		opacityControll();
	} 

	output.innerHTML = frameString;
	//console.log(frameString);
});


//Structure output
function concatData(id, data) {
	return id + ": " + data + "<br>";
}

//Prints the correct name
function getFingerName(fingerType) {
	switch(fingerType) {
		case 0:
			return 'Thumb';
		break;

		case 1:
			return 'Index';
		break;

		case 2:
			return 'Middle';
		break;

		case 3:
			return 'Ring';
		break;

		case 4:
			return 'Pinky';
		break;
	}
}


function concatJointPosition(id, position) {
	return id + ": " + position[0] + ", " + position[1] + ", " + position[2] + "<br>";
}


function cubeControll() {
	//console.log(roll);
	if (!sluggish) {
		roll = roll2;
		pitch = pitch2;
		yaw = yaw2;
	} else {

	}
	cube.style.transform = 'rotateZ(' + -roll + 'rad)' + 'rotateX(' + -pitch + 'rad)' + 'rotateY(' + -yaw + 'rad)';
	cube.style.webkitTransform = cube.style.MozTransform = cube.style.msTransform = cube.style.OTransform = cube.style.transform;
}

function opacityControll() {

	var outputMax = 1;
	var outputMin = 0;

	var inputMax = 350;
	var inputMin = 80;

	//Fix max/min vals
	if (lheight2 > inputMax) { 
		lheight2 = inputMax; 
	} else if (lheight2 < inputMin) { 
		lheight2 = inputMin; 
	}

	if (!sluggish) {
		percent = (lheight2 - inputMin) / (inputMax - inputMin);
		lheight = percent * (outputMax - outputMin) + outputMin;
	} else {

	}

	cube.style.opacity = lheight;
}

function valueReset(value, defaultValue, speed) {
	if (value == defaultValue || Math.abs(defaultValue - value) < speed) {
		return defaultValue;
	}
	if (value > defaultValue) {
		value = value - speed;
	} else if (value < defaultValue) {
		value = value + speed;
	}
	return value;
}




