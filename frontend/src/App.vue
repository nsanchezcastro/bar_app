<template>
  <div class="container">
    <h1>Staff Cocina</h1>

    <section class="card">
      <h2>Pedidos pendientes</h2>
      <button @click="fetchOrders" class="btn-refresh">🔄 Actualizar Lista</button>
      
      <ul v-if="orders.length" class="order-list">
        <li v-for="item in orders" :key="item.id" class="low-stock">
          <div class="order-info">
            <strong>{{ item.producto }}</strong>: Solo quedan {{ item.stock_actual }} unidades.
            <br>
            <small>Pedir {{ item.cantidad_a_pedir }} a {{ item.proveedor || 'Proveedor genérico' }}</small>
          </div>
          <button @click="marcarRecibido(item)" class="btn-action">✅ Recibido</button>
        </li>
      </ul>
      <p v-else class="empty-msg">El stock está al día. No hay pedidos pendientes.</p>
    </section>

    <section class="card">
      <h2>Añadir Nuevo Producto</h2>
      <div class="form-group">
        <input v-model="newProd.name" placeholder="Nombre del producto">
        <input v-model.number="newProd.stock" type="number" placeholder="Stock actual">
        <input v-model.number="newProd.min_stock" type="number" placeholder="Mínimo de seguridad">
        <input v-model="newProd.provider" placeholder="Proveedor">
        <button @click="addProduct" class="btn-add">➕ Añadir al Inventario</button>
      </div>
    </section>

    <section class="card">
      <h2>Tareas de Limpieza/Turno</h2>
      <div v-for="shift in tasks" :key="shift.id" class="shift-block">
        <h3>Turno: {{ shift.shift_name }}</h3>
        <ul>
          <li v-for="(task, index) in shift.checklist" :key="index" class="task-item">
            <input type="checkbox" v-model="task.done" @change="updateTask(shift)">
            <span :class="{ completed: task.done }">{{ task.item }}</span>
          </li>
        </ul>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const orders = ref([])
const tasks = ref([])
const newProd = ref({
  name: '',
  stock: 0,
  min_stock: 5,
  provider: ''
})


// Obtener pedidos pendientes
const fetchOrders = async () => {
  try {
    const res = await fetch('http://localhost:8000/orders/check')
    const data = await res.json()
    orders.value = data.lista_de_compra || []
  } catch (err) {
    console.error("Error al obtener pedidos:", err)
  }
}

// Obtener tareas
const fetchTasks = async () => {
  try {
    const res = await fetch('http://localhost:8000/tasks')
    const data = await res.json()
    tasks.value = data
  } catch (err) {
    console.error("Error al obtener tareas:", err)
  }
}

// Añadir producto 
const addProduct = async () => {
  if (!newProd.value.name) return alert("El nombre es obligatorio")

  try {
    const res = await fetch('http://localhost:8000/products', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        nombre: newProd.value.name,
        stock_actual: newProd.value.stock,
        stock_minimo: newProd.value.min_stock,
        proveedor: newProd.value.provider
      })
    })

    if (res.ok) {
      alert("¡Producto guardado!")
      newProd.value = { name: '', stock: 0, min_stock: 5, provider: '' }
      fetchOrders() // Recargar lista
    }
  } catch (err) {
    console.error("Error al guardar producto:", err)
  }
}

// Actualizar stock
const marcarRecibido = async (item) => {
  const cantidad = prompt(`¿Cuántas unidades de ${item.producto} han llegado?`, item.cantidad_a_pedir)
  if (cantidad) {
    try {
      await fetch(`http://localhost:8000/products/${item.id}/update-stock?added_stock=${cantidad}`, {
        method: 'PUT'
      })
      fetchOrders()
    } catch (err) {
      console.error("Error al actualizar stock:", err)
    }
  }
}

// Actualizar tarea (Checklist)
const updateTask = async (shift) => {
  console.log("Enviando actualización de tareas:", shift.checklist)
}

onMounted(() => {
  fetchOrders()
  fetchTasks()
})
</script>

<style>
.container { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; color: #333; }
h1 { text-align: center; color: #2c3e50; margin-bottom: 30px; }

.card { background: white; border: 1px solid #eee; padding: 25px; margin-bottom: 25px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
h2 { margin-top: 0; color: #34495e; border-bottom: 2px solid #42b983; display: inline-block; padding-bottom: 5px; }

.order-list { list-style: none; padding: 0; }
.low-stock { background: #fff5f5; border-left: 5px solid #ff4d4d; padding: 15px; margin: 10px 0; display: flex; justify-content: space-between; align-items: center; border-radius: 4px; }
.order-info { flex-grow: 1; }
.empty-msg { color: #666; font-style: italic; }

.form-group { display: flex; flex-direction: column; gap: 12px; margin-top: 15px; }
.form-group input { padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 16px; }

button { cursor: pointer; border: none; border-radius: 6px; transition: 0.3s; font-weight: bold; }
.btn-refresh { background: #ebf0f1; color: #2c3e50; padding: 8px 15px; margin-bottom: 15px; }
.btn-add { background: #2c3e50; color: white; padding: 12px; }
.btn-add:hover { background: #1a252f; }
.btn-action { background: #42b983; color: white; padding: 8px 12px; }

.task-item { list-style: none; margin: 8px 0; font-size: 17px; }
.completed { text-decoration: line-through; color: #bbb; }
.shift-block { margin-bottom: 20px; }
</style>