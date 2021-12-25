import {
  deleteDataAuth,
  getDataAuth,
  patchDataAuth,
  postDataAuth,
} from "./apiService";

export async function getTags() {
  return await getDataAuth("/api/tag/");
}

export async function getTag(id) {
  return await getDataAuth(`/api/tag/${id}/`);
}

export async function putTag(id, name, parent) {
  return await postDataAuth(`/api/tag/${id}/`, {
    name: name,
    parent: parent,
  });
}

export async function patchTag(id, data) {
  return await patchDataAuth(`/api/tag/${id}/`, data);
}

export async function postTag(data) {
  return await postDataAuth("/api/tag/", data);
}

export async function deleteTag(id) {
  return await deleteDataAuth(`/api/tag/${id}/`);
}
