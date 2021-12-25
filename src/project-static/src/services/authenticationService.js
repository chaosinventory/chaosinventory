import { getDataAuth, postData, postDataAuth } from "./apiService";

export const authenticationService = {
  login,
  getTokens,
  loggedIn,
  logout,
};

function login(username, password) {
  return new Promise((resolve, reject) => {
    postData("/api/authentication/token/credentials", {
      username: username,
      password: password,
      application: "chaosinventory",
    }).then((data) => {
      localStorage.setItem(import.meta.env.VITE_TOKEN_NAME, data.token);
      resolve("foo");
    });
  });
}

function loggedIn() {
  return true;
}

function renewToken() {}

function getTokens() {
  getDataAuth("/api/authentication/token").then((data) => {
    console.log(data);
  });
}

function logout() {
  localStorage.removeItem(import.meta.env.VITE_TOKEN_NAME);
}
