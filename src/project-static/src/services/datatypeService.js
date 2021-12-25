import {
  deleteDataAuth,
  getDataAuth,
  patchDataAuth,
  postDataAuth,
  putDataAuth,
} from "./apiService";

export async function getDatatypes() {
  return await getDataAuth("/api/datatype/");
}

export async function getDatatype(id) {
  return await getDataAuth(`/api/datatype/${id}/`);
}

export async function putDatatype(id, data) {
  return await putDataAuth(`/api/datatype/${id}/`, data);
}

export async function patchDatatype(id, data) {
  return await patchDataAuth(`/api/datatype/${id}/`, data);
}

export async function postDatatype(data) {
  return await postDataAuth("/api/datatype/", data);
}

export async function deleteDatatype(id) {
  return await deleteDataAuth(`/api/datatype/${id}/`);
}
