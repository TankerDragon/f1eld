const wrappers = document.getElementsByClassName("statusWrapper");
const controllers = document.getElementsByClassName("controller-rect");
const leftControllers = document.getElementsByClassName("control-left");
const timeStartBlocks = document.getElementsByClassName("time-start");
const rightControllers = document.getElementsByClassName("control-right");
const timeEndBlocks = document.getElementsByClassName("time-end");
const timeDurationBlocks = document.getElementsByClassName("time-duration");
const logShowers = document.getElementsByClassName("showBtn");
const tables = document.getElementsByClassName("main-table");

const applyButton = document.getElementById("applyBtn");
const cancelButton = document.getElementById("cancelBtn");
const startInput = document.getElementById("setStart");
const endInput = document.getElementById("setEnd");
//const edit = document.getElementById("edit");

var editCode,
  statusCode,
  nDaysBefore,
  nThStatus,
  startTimeChange,
  endTimeChange,
  durationTimeChange;

let showArray = [];
for (let i = 0; i < logShowers.length; i++) {
  showArray[i] = false;
}

function displayController(n1, n2) {
  // closing controller-rect that opened before

  //
  if (n2 == 0) {
    if (status_information[n1].length == 0) {
      if (n1 == 0) {
        controllers[n1].style.width =
          (stringtimetoSeconds(current_time) * 100) / (24 * 60 * 60) + "%";
      } else {
        controllers[n1].style.width = "100%";
      }
    } else {
      controllers[n1].style.width =
        (status_information[n1][n2][1] * 100) / (24 * 60 * 60) + "%";
    }
  } else {
    controllers[n1].style.width =
      (status_information[n1][n2 - 1][2] * 100) / (24 * 60 * 60) + "%";
  }
  if (n2 == 0) {
    controllers[n1].style.left = 0 + "%";
  } else {
    controllers[n1].style.left =
      (status_information[n1][n2 - 1][1] * 100) / (24 * 60 * 60) + "%";
  }

  controllers[n1].style.display = "block";

  if (n2 == 0) {
    controllers[n1].style.backgroundColor = controller_colors[before_class[n1]];
  } else {
    controllers[n1].style.backgroundColor =
      controller_colors[status_information[n1][n2 - 1][0]];
  }

  // start time
  if (n2 == 0) {
    timeStartBlocks[n1].innerText = "<<";
    leftControllers[n1].style.display = "none";
  } else {
    timeStartBlocks[n1].innerText = secondToStringTime(
      status_information[n1][n2 - 1][1]
    );
  }

  // end time
  if (n2 == status_information[n1].length) {
    if (n1 == 0) {
      timeEndBlocks[n1].innerText = secondToStringTime(
        stringtimetoSeconds(current_time)
      );
    } else {
      timeEndBlocks[n1].innerText = ">>";
      rightControllers[n1].style.display = "none";
    }
  } else {
    timeEndBlocks[n1].innerText = secondToStringTime(
      status_information[n1][n2][1]
    );
  }

  // time duration

  if (status_information[n1].length == 0) {
    if (dayChangeDurations[n1] == -1) {
      timeDurationBlocks[n1].innerText = "no enough data";
    } else {
      timeDurationBlocks[n1].innerText = secondToStringDurationTime(
        dayChangeDurations[n1]
      );
    }
  } else if (n2 == 0) {
    if (
      dayChangeDurations[n1 + 1] == -1 ||
      n1 == status_information.length - 1
    ) {
      timeDurationBlocks[n1].innerText = "no enough data";
    } else {
      timeDurationBlocks[n1].innerText = secondToStringDurationTime(
        dayChangeDurations[n1 + 1]
      );
    }
  } else if (n1 != 0 && n2 == status_information[n1].length) {
    timeDurationBlocks[n1].innerText = secondToStringDurationTime(
      dayChangeDurations[n1]
    );
  } else {
    timeDurationBlocks[n1].innerText = secondToStringDurationTime(
      status_information[n1][n2 - 1][2]
    );
  }
}

function clear() {
  for (let j = 0; j < current_data.length; j++) {
    controllers[j].style.display = "none";
    leftControllers[j].style.display = "block";
    rightControllers[j].style.display = "block";
  }
}
var currentWrapper;
var indexLeft, indexRight;

for (let i = 0; i < wrappers.length; i++) {
  currentWrapper = wrappers[i];
  currentWrapper.addEventListener("click", function (e) {
    var index1 = Array.prototype.indexOf.call(
      this.parentElement.parentElement.parentElement.children,
      this.parentElement.parentElement
    );
    var index2 = Array.prototype.indexOf.call(this.children, e.target);

    if (
      index1 >= 0 &&
      index1 <= status_information.length &&
      index2 >= 0 &&
      index2 <= status_information[index1].length
    ) {
      clear();

      nDaysBefore = index1;
      nThStatus = index2;

      displayController(index1, index2);
      indexLeft = index1;
      indexRight = index1;

      if (index2 == 0) {
        for (let j = index1 + 1; j < status_information.length; j++) {
          displayController(j, status_information[j].length);
          if (status_information[j] != 0) {
            indexLeft = j;
            break;
          }
        }
      }
      if (index1 != 0 && index2 == status_information[index1].length) {
        for (let j = index1 - 1; j >= 0; j--) {
          displayController(j, 0);
          if (status_information[j] != 0) {
            indexRight = j;
            break;
          }
        }
      }
      dragElement(controllers[index1]);
    }
  });
}

////////////////Make the DIV element draggagle:

function dragElement(elmnt) {
  var pos1 = 0,
    pos2 = 0,
    parentWidth1 = 0,
    parentWidth2 = 0;

  // if present, the header is where you move the DIV from:
  leftControllers[indexLeft].onmousedown = dragMouseDownLeft;
  rightControllers[indexRight].onmousedown = dragMouseDownRight;

  function dragMouseDownLeft(e) {
    parentWidth1 = controllers[indexLeft].parentElement.offsetWidth;

    e = e || window.event;
    e.preventDefault();
    // get the mouse cursor position at startup:
    pos2 = e.clientX;
    document.onmouseup = closeDragElement;
    // call a function whenever the cursor moves:
    document.onmousemove = elementDragLeft;
  }
  function dragMouseDownRight(e) {
    parentWidth2 = controllers[indexRight].parentElement.offsetWidth;

    e = e || window.event;
    e.preventDefault();
    // get the mouse cursor position at startup:
    pos2 = e.clientX;
    document.onmouseup = closeDragElement;
    // call a function whenever the cursor moves:
    document.onmousemove = elementDragRight;
  }

  function elementDragLeft(e) {
    e = e || window.event;
    e.preventDefault();
    // calculate the new cursor position:
    pos1 = pos2 - e.clientX;
    pos2 = e.clientX;
    // set the element's new position:

    if (controllers[indexLeft].offsetWidth + pos1 >= 4) {
      if (controllers[indexLeft].offsetLeft - pos1 < 0) {
        controllers[indexLeft].style.left = 0;
        startTimeChange = percentToStringtime(0);
      } else {
        controllers[indexLeft].style.left =
          ((controllers[indexLeft].offsetLeft - pos1) / parentWidth1) * 100 +
          "%";
        controllers[indexLeft].style.width =
          ((controllers[indexLeft].offsetWidth + pos1) / parentWidth1) * 100 +
          "%";
        startTimeChange = percentToStringtime(
          ((controllers[indexLeft].offsetLeft - pos1) / parentWidth1) * 100
        );
      }

      //console.log(elmnt);

      timeStartBlocks[indexLeft].innerText = startTimeChange;
    }
  }
  function elementDragRight(e) {
    e = e || window.event;
    e.preventDefault();
    // calculate the new cursor position:
    pos1 = pos2 - e.clientX;
    pos2 = e.clientX;
    // set the element's new position:

    if (
      controllers[indexRight].offsetLeft +
        controllers[indexRight].offsetWidth -
        pos1 <=
      parentWidth2
    ) {
      controllers[indexRight].style.width =
        ((controllers[indexRight].offsetWidth - pos1) / parentWidth2) * 100 +
        "%";
      endTimeChange = percentToStringtime(
        ((controllers[indexRight].offsetLeft +
          controllers[indexRight].offsetWidth -
          pos1) /
          parentWidth2) *
          100
      );
    } else {
      endTimeChange = percentToStringtime(100);
    }

    timeEndBlocks[indexRight].innerText = endTimeChange;
  }

  function closeDragElement() {
    // stop moving when mouse button is released:
    document.onmouseup = null;
    document.onmousemove = null;
  }
}

cancelButton.addEventListener("click", () => {
  clear();
});
applyButton.addEventListener("click", () => {
  window.alert("error: NO CONNECTION WITH SERVER");
});
for (let i = 0; i < logShowers.length; i++) {
  logShowers[i].addEventListener("click", () => {
    if (showArray[i] == true) {
      showArray[i] = false;
      tables[i].style.display = "none";
    } else {
      showArray[i] = true;
      tables[i].style.display = "table";
    }
  });
}
for (let i = 0; i < logShowers.length; i++) {
  if (informations[i].length == 0) {
    logShowers[i].style.display = "none";
  }
}

var c = document.getElementsByClassName("myCanvas");
arr = ["#ffbb00", "#00b51e", "#00cce3", "#0083ff"];
for (let i = 0; i < 4; i++) {
  var ctx = c[i].getContext("2d");
  ctx.beginPath();
  ctx.lineWidth = 5;
  ctx.strokeStyle = arr[i];
  ctx.arc(50, 50, 45, 0, 2 * Math.PI);
  ctx.stroke();
}
