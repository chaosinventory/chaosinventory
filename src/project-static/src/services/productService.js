import { getDataAuth, postDataAuth } from "./apiService";

export async function getProducts() {
  return await getDataAuth("/api/product/");
}

export async function getProduct(id) {
  return await getDataAuth(`/api/product/${id}/`);
}

export async function postProduct(data) {
  return await postDataAuth("/api/product/", data);
}

export async function patchProduct(id, data) {
  return await patchDataAuth(`/api/product/${id}/`, data);
}
