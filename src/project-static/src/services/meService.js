import {
  getDataAuth,
} from "./apiService";

export async function getMe() {
  return await getDataAuth("/api/me/");
}
