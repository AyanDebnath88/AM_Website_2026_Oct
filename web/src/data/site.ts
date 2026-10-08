export const site = {
  name: 'AM Electricals',
  tagline: 'Control Panel Manufacturer since 1991',
  established: 1991,
  yearsInBusiness: new Date().getFullYear() - 1991,
  founder: 'Ajit Debnath',
  phone: '+91-7003707013',
  phoneRaw: '917003707013',
  email: 'amelectricals@yahoo.co.in',
  address: {
    street: '7S Kamardanga Road, Near Anandapalit',
    city: 'Kolkata',
    postcode: '700046',
    state: 'West Bengal',
    country: 'India',
  },
  factorySqft: 5000,
  certifications: [
    { name: 'CPRI 6000A', short: 'CPRI', description: 'Central Power Research Institute type-tested at 6000A' },
    { name: 'ISO 9001:2008', short: 'ISO', description: 'Quality Management System certified' },
  ],
  social: {
    whatsapp: 'https://wa.me/917003707013',
    linkedin: '',
  },
  whatsappPrefill: (subject: string = 'Panel enquiry') =>
    `https://wa.me/917003707013?text=${encodeURIComponent(`Hello AM Electricals, I am enquiring about: ${subject}`)}`,
} as const;

export const nav = {
  primary: [
    { label: 'Home', href: '/' },
    { label: 'Panels', href: '/panels/', hasMega: true },
    { label: 'Industries', href: '/industries/', hasMega: true },
    { label: 'About', href: '/about/' },
    { label: 'Careers', href: '/careers/' },
    { label: 'Contact', href: '/contact/' },
  ],
  cta: { label: 'Get Free Quote', href: '/quote/' },
} as const;

export const googleForm = {
  actionUrl: 'https://docs.google.com/forms/d/e/1FAIpQLSf2jjecUl1tkBKU-2F6WTSlaMWSNVPseQym3uFvZOp9oPwjNw/formResponse',
  entries: {
    name: 'entry.2136778375',
    phone: 'entry.14751728',
    email: 'entry.224303003',
    panel: 'entry.27978173',
    message: 'entry.611094286',
  },
} as const;
