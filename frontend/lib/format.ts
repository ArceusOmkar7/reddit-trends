const normalizeIso = (value: string) => {
  if (/^\d{4}-\d{2}-\d{2}T\d{2}$/.test(value)) {
    return `${value}:00:00Z`;
  }
  if (/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$/.test(value)) {
    return `${value}:00Z`;
  }
  return value;
};

export const formatLocalTime = (value: string) => {
  const date = new Date(normalizeIso(value));
  if (Number.isNaN(date.getTime())) {
    return value;
  }
  return new Intl.DateTimeFormat(undefined, {
    hour: "2-digit",
    minute: "2-digit"
  }).format(date);
};

export const formatLocalDateTime = (value: string) => {
  const date = new Date(normalizeIso(value));
  if (Number.isNaN(date.getTime())) {
    return value;
  }
  return new Intl.DateTimeFormat(undefined, {
    dateStyle: "medium",
    timeStyle: "short"
  }).format(date);
};
