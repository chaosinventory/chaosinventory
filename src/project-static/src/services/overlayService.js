import {
  deleteDataAuth,
  getDataAuth,
  patchDataAuth,
  postDataAuth,
} from "./apiService";

export async function getOverlays() {
  return await getDataAuth("/api/overlay/");
}

export async function getOverlay(id) {
  return await getDataAuth(`/api/overlay/${id}/`);
}

export async function putOverlay(id, data) {
  return await postDataAuth(`/api/overlay/${id}/`, data);
}

export async function patchOverlay(id, data) {
  return await patchDataAuth(`/api/overlay/${id}/`, data);
}

export async function postOverlay(data) {
  return await postDataAuth("/api/overlay/", data);
}

export async function deleteOverlay(id) {
  return await deleteDataAuth(`/api/overlay/${id}/`);
}
