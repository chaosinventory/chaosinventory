import Cookies from 'js-cookie';

export async function getDataAuth(url = "") {
  const response = await fetch(url, {
    method: "GET",
    mode: "cors",
    // cache: "force-cache",
    credentials: "same-origin",
    headers: {
      "Content-Type": "application/json",
    },
    redirect: "follow",
    referrerPolicy: "no-referrer",
  });

  return new Promise((resolve, reject) => {
    if (response.ok) {
      resolve(response.json());
    } else {
      if (response.status === 403) {
        document.location.href = "/login/?next=" + window.location.pathname;
      }
      reject(new Error("request failed"));
    }
  });
}

export async function postDataAuth(url = "", data = {}) {
  return apiInteractionAuth(url, data, "POST");
}

export async function putDataAuth(url = "", data = {}) {
  return apiInteractionAuth(url, data, "PUT");
}

export async function patchDataAuth(url = "", data = {}) {
  return apiInteractionAuth(url, data, "PATCH");
}

export async function deleteDataAuth(url = "", data = {}) {
  return apiInteractionAuth(url, data, "DELETE");
}

async function apiInteractionAuth(url = "", data = {}, method = "POST") {
  const response = await fetch(url, {
    method: method,
    mode: "cors",
    cache: "no-cache",
    credentials: "same-origin",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": Cookies.get('csrftoken'),
    },
    redirect: "follow",
    referrerPolicy: "no-referrer",
    body: JSON.stringify(data),
  });

  return new Promise((resolve, reject) => {
    if (response.ok) {
      resolve(response.json());
    } else {
      reject(new Error("request failed"));
    }
  });
}
