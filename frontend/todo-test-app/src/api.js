const BASE_URL = 'http://localhost:3001/';

export const API_ENDPOINTS = {
  COURSES_LIST: `${BASE_URL}/courses/`, // GET (список) или POST (создание)
  COURSE_DETAIL: (id) => `${BASE_URL}/courses/${id}/`, // GET, PUT, DELETE
};
