function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
}

class Api {
    constructor(apiUrl) {
        this.apiUrl =  apiUrl;
        this.headers = {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie("csrftoken"),
        };
    }
  async getPurchases() {
    const e = await fetch(`${this.apiUrl}/purchases/`, {
      headers: {
        'Content-Type': 'application/json'
      }
    });
    if (e.ok) {
      return e.json();
    }
    return await Promise.reject(e.statusText);
  }
  async addPurchases(id) {
    const e = await fetch(`${this.apiUrl}/purchases/`, {
      method: 'POST',
      headers: this.headers,
      body: JSON.stringify({
        recipe: id
      })
    });
    if (e.ok) {
      return e.json();
    }
    return await Promise.reject(e.statusText);
  }
  async removePurchases(id) {
    const e = await fetch(`${this.apiUrl}/purchases/${id}/`, {
      method: 'DELETE',
      headers: this.headers,
    });
    if (e.ok) {
      return e.json();
    }
    return await Promise.reject(e.statusText);
  }
  async addSubscriptions(username) {
    const e = await fetch(`${this.apiUrl}/subscribe/`, {
      method: 'POST',
      headers: this.headers,
      body: JSON.stringify({
        author: username
      })
    });
    if (e.ok) {
      return e.json();
    }
    return await Promise.reject(e.statusText);
  }
  async removeSubscriptions(id) {
    const e = await fetch(`${this.apiUrl}/subscribe/${id}/`, {
      method: 'DELETE',
      headers: this.headers,
    });
    if (e.ok) {
      return e.json();
    }
    return await Promise.reject(e.statusText);
  }
  async addFavorites(id) {
    const e = await fetch(`${this.apiUrl}/favorites/`, {
      method: 'POST',
      headers: this.headers,
      body: JSON.stringify({
        recipe: id
      })
    });
    if (e.ok) {
      return e.json();
    }
    return await Promise.reject(e.statusText);
  }
  async removeFavorites (id) {
    const e = await fetch(`${this.apiUrl}/favorites/${id}/`, {
      method: 'DELETE',
      headers: this.headers,
    });
    if (e.ok) {
      return e.json();
    }
    return await Promise.reject(e.statusText);
  }
    async getIngredients(text) {
        const e = await fetch(`${this.apiUrl}/ingredients/?query=${text}`, {
          headers: this.headers,
      });
      if (e.ok) {
        return e.json();
      }
      return await Promise.reject(e.statusText);
    }
}
