function Ajax_request(route) {
  const display_div = document.getElementById("display");
  const loader = document.getElementById("loader");
  var xhr = new XMLHttpRequest();
  display_div.style.display = "none";
  loader.style.display = "flex";
  xhr.open("GET", `/api/get/addr/${route}`, true);
  xhr.onreadystatechange = function () {
    if (xhr.readyState == 4) {
      if (xhr.status == 200) {
        display_div.innerHTML = xhr.responseText;
        display_div.style.display = "block";
        loader.style.display = "none";
        if (route == "home") {
          onpageload();
        }
        bindEventListeners(); // Rebind event listeners
      } else {
        console.log("Error fetching data");
      }
    }
  };
  xhr.send();
}

function UserAvailability(route) {
  var xhr = new XMLHttpRequest();
  xhr.open("GET", `api/userstate/${route}`);
  xhr.send();
}

function Ajax_Order_request(state) {
  const display_div = document.getElementById("orderbox");
  const loader = document.getElementById("loader");
  display_div.style.display = "none";
  loader.style.display = "flex";
  loader.classList.remove("h-[100vh]");
  loader.classList.add("h-[20vh]");
  var xhr = new XMLHttpRequest();
  xhr.open("GET", `/api/get/state/${state}`, true);
  xhr.onreadystatechange = function () {
    if (xhr.readyState == 4) {
      if (xhr.status == 200) {
        display_div.innerHTML = xhr.responseText;
        display_div.style.display = "block";
        loader.style.display = "none";
        loader.classList.add("h-[100vh]");
        loader.classList.remove("h-[20vh]");
        bindEventListeners(); // Rebind event listeners
      } else {
        console.log("Error fetching data");
      }
    }
  };
  xhr.send();
}

function Block_disable(priority) {
  let home = document.getElementById("b-home");
  let order = document.getElementById("b-order");
  let notification = document.getElementById("b-notification");
  let profile = document.getElementById("b-profile");
  home.style.color = priority == "home" ? "Black" : "Gray";
  order.style.color = priority == "orders" ? "Black" : "Gray";
  notification.style.color = priority == "notifications" ? "Black" : "Gray";
  profile.style.color = priority == "profile" ? "Black" : "Gray";
}

// Initial binding of event listeners
window.addEventListener("load", () => {
  bindEventListeners();
});

const Activity = () => {
  var check = document.getElementById("toggleFour");
  var status_text = document.getElementById("status_active");
  var clock = document.getElementById("clock");
  if (check.checked) {
    status_text.textContent = "Inactive";
    sessionStorage.removeItem("Active");
    clock.style.display = "none";
    clock.style.transition = "1s ease in";
    UserAvailability("inactive");
  } else {
    status_text.textContent = "Active";
    sessionStorage.setItem("Active", "true");
    clock.style.display = "flex";
    clock.style.transition = "1s ease in";
    clocked();
    UserAvailability("active");
  }
};

const clocked = () => {
  let hour = document.getElementById("hr");
  let minute = document.getElementById("min");
  let second = document.getElementById("sec");

  setInterval(() => {
    const now = new Date();
    let hr = now.getHours();
    let min = now.getMinutes();
    let sec = now.getSeconds();

    hour.textContent = hr.toString().length === 1 ? "0" + hr : hr;
    minute.textContent = min.toString().length === 1 ? "0" + min : min;
    second.textContent = sec.toString().length === 1 ? "0" + sec : sec;
  }, 1000);
};

function bindEventListeners() {
  try {
    var backbtn = document.getElementById("backbtn");
    backbtn.addEventListener("click", () => {
      Update_Page("home");
    });
  } catch (error) {}
  try {
    document
      .getElementById("notification_box")
      .addEventListener("click", () => {
        Update_Page("notifications");
      });
  } catch (error) {}
}

const greet = () => {
  let greeting = document.getElementById("greetings");
  const time = new Date();
  let hour = time.getHours();
  if (hour >= 0 && hour < 12) {
    greeting.textContent = "Good Morning,";
  } else if (hour >= 12 && hour < 16) {
    greeting.textContent = "Good Afternoon,";
  } else if (hour >= 16 && hour < 19) {
    greeting.textContent = "Good Evening,";
  } else {
    greeting.textContent = "Happy Night,";
  }
};

function onpageload() {
  if (sessionStorage.getItem("Active") == "true") {
    document.getElementById("toggleFour").checked = false;
    document.getElementById("status_active").textContent = "Active";
    var clock = document.getElementById("clock");
    clock.style.display = "flex";
    clock.style.transition = "1s ease in";
    clocked();
    UserAvailability("active");
  } else {
    UserAvailability("inactive");
  }
  greet();
}

const Update_Page = (page) => {
  Block_disable(page);
  Ajax_request(page);
};

window.addEventListener("load", () => {
  onpageload();
});

document.getElementById("home-div").addEventListener("click", () => {
  Update_Page("home");
});
document.getElementById("order-div").addEventListener("click", () => {
  Update_Page("orders");
});
document.getElementById("notification-div").addEventListener("click", () => {
  Update_Page("notifications");
});
document.getElementById("profile-div").addEventListener("click", () => {
  Update_Page("profile");
});

window.addEventListener("load", () => {
  bindEventListeners();
});

const switchState = (state) => {
  document.getElementById("pending").style.color =
    state == "pending" ? "black" : "gray";
  document.getElementById("past").style.color =
    state == "past" ? "black" : "gray";

  Ajax_Order_request(state);
};

const view_order = (order_number) => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const currentLat = position.coords.latitude;
        const currentLng = position.coords.longitude;
        var final_str = `perticular/order/initial,${order_number},${currentLat},${currentLng}`;
        Ajax_request(final_str);
      },
      (error) => {
        console.error("Error getting the current location:", error);
      }
    );
  } else {
    console.error("Geolocation is not supported by this browser.");
  }
};

const Order_Next = (orderno, nextState) => {
  if (nextState == "accepted") {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const currentLat = position.coords.latitude;
          const currentLng = position.coords.longitude;
          var final_str = `perticular/order/accepted,${orderno},${currentLat},${currentLng}`;
          Ajax_request(final_str);
        },
        (error) => {
          console.error("Error getting the current location:", error);
        }
      );
    } else {
      console.error("Geolocation is not supported by this browser.");
    }
  } else if (nextState == "picked") {
    var final_str = `perticular/order/picked,${orderno}`;
    Ajax_request(final_str);
  } else if (nextState == "delievered") {
    var final_str = `perticular/order/delievered,${orderno}`;
    Ajax_request(final_str);
  }
};
