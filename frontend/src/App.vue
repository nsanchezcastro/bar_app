<template>
  <div class="container">
    <h1>Staff Cocina</h1>

    <section class="card">
      <h2>Pedidos pendientes</h2>
      <button @click="fetchOrders">Actualizar Stock</button>
      <ul v-if="orders.length">
        <li v-for="item in orders" :key="item.producto" class="low-stock">
          <strong>{{ item.producto }}</strong>: Solo quedan {{ item.stock_actual }} 
          <span>(Pedir {{ item.cantidad_a_pedir }} a {{ item.proveedor }})</span>
        </li>
      </ul>
      <p v-else>El stock está al día.</p>
    </section>

    <section class="card">
      <h2>Tareas</h2>
      <div v-for="shift in tasks" :key="shift.id">
        <h3>Turno: {{ shift.shift_name }}</h3>
        <ul>
          <li v-for="(task, index) in shift.checklist" :key="index">
            <input type="checkbox" v-model="task.done" @change="updateTask(shift)">
            <span :class="{ completed: task.done }">{{ task.item }}</span>
          </li>
        </ul>
      </div>
    </section>

    <section class="card">
  <h2>Añadir Nuevo Producto</h2>
  <div class="form-group">
    <input v-model="newProd.name" placeholder="Nombre">
    <input v-model.number="newProd.stock" type="number" placeholder="Stock actual">
    <input v-model.number="newProd.min_stock" type="number" placeholder="Mínimo seguridad">
    <input v-model="newProd.provider" placeholder="Proveedor">
    <button @click="addProduct">Añadir al Inventario</button>
  </div>
</section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const orders = ref([])
const tasks = ref([])

// Obtener pedidos 
const fetchOrders = async () => {
  const res = await fetch('http://localhost:8000/orders/check')
  const data = await res.json()
  orders.value = data.lista_de_compra

}

// Obtener tareas 
const fetchTasks = async () => {
  const res = await fetch('http://localhost:8000/tasks')
  const data = await res.json()
  tasks.value = data
}

// Actualizar tarea 
const updateTask = async (shift) => {
  console.log("Enviando actualización de JSONB:", shift.checklist)
}

onMounted(() => {
  fetchOrders()
  fetchTasks()
})

const newProd = ref({
  name: '',
  stock: 0,
  min_stock: 5,
  provider: ''
})

const addProduct = async () => {
  if (!newProd.value.name) return alert("Ponle un nombre al producto")

  // URL con parámetros 
  const url = `http://localhost:8000/products?name=${newProd.value.name}&stock=${newProd.value.stock}&min_stock=${newProd.value.min_stock}&provider_name=${newProd.value.provider}`
  
  try {
    const res = await fetch(url, { method: 'POST' })
    if (res.ok) {
      alert("¡Producto guardado!")
      // Limpiar formulario
      newProd.value = { name: '', stock: 0, min_stock: 5, provider: '' }
      // Actualizar la lista 
      fetchOrders()
    }
  } catch (err) {
    console.error("Error al guardar producto:", err)
  }
}

const editStock = async (item) => {
  const nuevoStock = prompt(`Nuevo stock para ${item.producto}:`, item.stock_actual)
  if (nuevoStock !== null) {
    await fetch(`http://localhost:8000/products/${item.id}?name=${item.producto}&stock=${nuevoStock}`, {
      method: 'PUT'
    })
    fetchOrders() // Refrescar lista
  }
}
</script>

<style>
.container { font-family: sans-serif; max-width: 800px; margin: auto; }
.card { border: 1px solid #ddd; padding: 20px; margin-bottom: 20px; border-radius: 8px; }
.low-stock { color: #d9534f; background: #f9f2f2; padding: 5px; margin: 5px 0; }
.completed { text-decoration: line-through; color: gray; }
h1 { text-align: center; color: #2c3e50; }
button { background: #42b983; color: white; border: none; padding: 10px; cursor: pointer; }
</style>
