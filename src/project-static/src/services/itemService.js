import {
  deleteDataAuth,
  getDataAuth,
  patchDataAuth,
  postDataAuth,
} from "./apiService";

export async function getItems() {
  return await getDataAuth("/api/item/");
}

export async function getItem(id) {
  return await getDataAuth(`/api/item/${id}/`);
}

export async function putItem(id, data) {
  return await postDataAuth(`/api/item/${id}/`, data);
}

export async function patchItem(id, data) {
  return await patchDataAuth(`/api/item/${id}/`, data);
}

export async function postItem(data) {
  return await postDataAuth("/api/item/", data);
}

export async function deleteItem(id) {
  return await deleteDataAuth(`/api/item/${id}/`);
}
