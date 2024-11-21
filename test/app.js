async function fetchData() {
  try {
    function getCsrfToken() {
      let cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        let cookie = cookies[i].trim();
        let [name, value] = cookie.split("=");
        if (name === "csrftoken") {
          return value;
        }
      }
      return null;
    }
    let csrftoken = getCsrfToken();
    const email = "madhan@gmail.com";
    const password = "maxx5422i";

    const suData = async () => {
      const response = await fetch("http://localhost:8000/api/login/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();
      console.log(data)
    };

    return suData;
  } catch (error) {
    console.error("Error:", error);
  }
}

window.onload = async function() {
  const submitData = await fetchData();
  document.getElementById("button").onclick = submitData;
}