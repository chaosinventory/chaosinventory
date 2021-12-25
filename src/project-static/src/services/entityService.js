import {
  deleteDataAuth,
  getDataAuth,
  patchDataAuth,
  postDataAuth,
} from "./apiService";

export async function getEntities() {
  return await getDataAuth("/api/entity/");
}

export async function getEntity(id) {
  return await getDataAuth(`/api/entity/${id}/`);
}

export async function putEntity(id, data) {
  return await postDataAuth(`/api/entity/${id}/`, data);
}

export async function patchEntity(id, data) {
  return await patchDataAuth(`/api/entity/${id}/`, data);
}

export async function postEntity(data) {
  return await postDataAuth("/api/entity/", data);
}

export async function deleteEntity(id) {
  return await deleteDataAuth(`/api/entity/${id}/`);
}
