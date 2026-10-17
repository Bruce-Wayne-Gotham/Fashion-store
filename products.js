/*
 * ─────────────────────────────────────────────────────────────
 *  YOUR AFFILIATE SETUP — edit this file only.
 * ─────────────────────────────────────────────────────────────
 *
 *  1. STORES: put your affiliate homepage / campaign link for each store.
 *  2. AMAZON_TAG: your Amazon Associates tracking ID (e.g. "yourname-21").
 *     It is appended automatically to every amazon.in link that lacks a tag.
 *  3. PRODUCTS: paste the affiliate deep link you generated for each product
 *     (Amazon SiteStripe, Myntra/Ajio via EarnKaro, Cuelinks, Admitad, etc.)
 *     into `url`. `image` can be a product photo URL from the store, or one of
 *     the bundled illustrations in images/ (used by default so the page always
 *     has visuals, even offline).
 *
 *  Anything still pointing at a plain store URL will work, it just won't earn.
 */

window.AFFILIATE_CONFIG = {
  AMAZON_TAG: "", // e.g. "brucewayne-21"

  STORES: {
    myntra: {
      name: "Myntra",
      tagline: "India's fashion destination",
      url: "https://www.myntra.com/", // ← your Myntra affiliate link
      color: "#ff3f6c",
    },
    amazon: {
      name: "Amazon",
      tagline: "Fast delivery, endless choice",
      url: "https://www.amazon.in/fashion", // ← your Amazon affiliate link
      color: "#ff9900",
    },
    ajio: {
      name: "AJIO",
      tagline: "Handpicked. Trend-first.",
      url: "https://www.ajio.com/", // ← your AJIO affiliate link
      color: "#2c4152",
    },
  },

  PRODUCTS: [
    {
      title: "Oversized Linen Shirt",
      brand: "Roadster",
      store: "myntra",
      category: "Men",
      price: 1199,
      mrp: 2399,
      badge: "Bestseller",
      image: "images/linen-shirt.svg",
      url: "https://www.myntra.com/shirts",
    },
    {
      title: "Floral Wrap Midi Dress",
      brand: "SASSAFRAS",
      store: "myntra",
      category: "Women",
      price: 1349,
      mrp: 2999,
      badge: "New",
      image: "images/wrap-dress.svg",
      url: "https://www.myntra.com/dresses",
    },
    {
      title: "Air Cushion Running Sneakers",
      brand: "Puma",
      store: "amazon",
      category: "Footwear",
      price: 3499,
      mrp: 6999,
      badge: "Deal",
      image: "images/running-sneakers.svg",
      url: "https://www.amazon.in/s?k=puma+running+shoes",
    },
    {
      title: "Classic Leather Tote",
      brand: "Lavie",
      store: "amazon",
      category: "Accessories",
      price: 1899,
      mrp: 4250,
      badge: "",
      image: "images/leather-tote.svg",
      url: "https://www.amazon.in/s?k=leather+tote+bag",
    },
    {
      title: "Relaxed Denim Jacket",
      brand: "LEVIS",
      store: "ajio",
      category: "Men",
      price: 2799,
      mrp: 4599,
      badge: "Trending",
      image: "images/denim-jacket.svg",
      url: "https://www.ajio.com/s/denim-jackets",
    },
    {
      title: "Ribbed Knit Co-ord Set",
      brand: "AJIO Life",
      store: "ajio",
      category: "Women",
      price: 1599,
      mrp: 3199,
      badge: "New",
      image: "images/knit-coord.svg",
      url: "https://www.ajio.com/s/co-ords",
    },
    {
      title: "Minimal Chronograph Watch",
      brand: "Fossil",
      store: "amazon",
      category: "Accessories",
      price: 6995,
      mrp: 10995,
      badge: "",
      image: "images/chronograph-watch.svg",
      url: "https://www.amazon.in/s?k=fossil+chronograph",
    },
    {
      title: "Everyday Crew Tee — Pack of 3",
      brand: "HRX",
      store: "myntra",
      category: "Men",
      price: 899,
      mrp: 1999,
      badge: "Value",
      image: "images/crew-tees.svg",
      url: "https://www.myntra.com/tshirts",
    },
    {
      title: "Block Heel Mules",
      brand: "Mochi",
      store: "ajio",
      category: "Footwear",
      price: 1490,
      mrp: 2490,
      badge: "",
      image: "images/block-mules.svg",
      url: "https://www.ajio.com/s/women-heels",
    },
    {
      title: "Aviator Sunglasses",
      brand: "Ray-Ban",
      store: "myntra",
      category: "Accessories",
      price: 5590,
      mrp: 7990,
      badge: "Premium",
      image: "images/aviator-sunglasses.svg",
      url: "https://www.myntra.com/sunglasses",
    },
    {
      title: "Tailored Wool Blazer",
      brand: "Van Heusen",
      store: "amazon",
      category: "Men",
      price: 4299,
      mrp: 8999,
      badge: "",
      image: "images/wool-blazer.svg",
      url: "https://www.amazon.in/s?k=men+blazer",
    },
    {
      title: "Pleated Satin Skirt",
      brand: "Forever New",
      store: "ajio",
      category: "Women",
      price: 2199,
      mrp: 4399,
      badge: "",
      image: "images/satin-skirt.svg",
      url: "https://www.ajio.com/s/skirts",
    },
  ],
};
