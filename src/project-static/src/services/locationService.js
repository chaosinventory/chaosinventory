import {
  deleteDataAuth,
  getDataAuth,
  patchDataAuth,
  postDataAuth,
} from "./apiService";

export async function getLocations() {
  return await getDataAuth("/api/location/");
}

export async function getLocation(id) {
  return await getDataAuth(`/api/location/${id}/`);
}

export async function putLocation(id, data) {
  return await postDataAuth(`/api/location/${id}/`, data);
}

export async function patchLocation(id, data) {
  return await patchDataAuth(`/api/location/${id}/`, data);
}

export async function postLocation(data) {
  return await postDataAuth("/api/location/", data);
}

export async function deleteLocation(id) {
  return await deleteDataAuth(`/api/location/${id}/`);
}
